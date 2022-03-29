import os
import glob
import copy

import numpy as np

import configuration
import convert
import util
import utils.io
import infofile_utils
import intrinsics
import utils.io


def get_opticalib(dataset_dir):
    opticalib_path = os.path.join(dataset_dir, 'opticalib.json')
    if os.path.isfile(opticalib_path):
        opticalib = utils.io.load_json(opticalib_path)
        calib_info = opticalib.get('Scene', None)
    else:
        calib_info = None
    return calib_info


def get_calib_from_opticalib(calib_info):
    """Convert Scene dict from opticalib.json to the optitrack calibration dict that is usually in an infofile"""
    calibration = {
        'R': calib_info['camera']['R'],
        't': calib_info['camera']['t'],
        'cX': calib_info['camera']['cX'],
        'cY': calib_info['camera']['cY'],
        'fX': calib_info['camera']['fX'],
        'fY': calib_info['camera']['fY'],
        'k': calib_info['camera']['k'],
        'p': calib_info['camera']['p'],
        'forwardPose': [calib_info['forwardPose']['noseVector'], calib_info['forwardPose']['rightEarVector'],
                        calib_info['forwardPose']['spineVector']]
    }
    volume = calib_info['volumes'][0]
    if 'center' in volume:
        calibration['center'] = volume['center']
        calibration['extent'] = (2. * np.array(volume['extent'])).tolist()
    else:
        x, y, z = [volume['x1'], volume['x2']], [volume['y1'], volume['y2']], [volume['z1'], volume['z2']],
        center_extent = convert.volume_to_center_extent(x, y, z, as_dict=True)
        calibration.update(center_extent)

    return calibration


def _verify_video_file(video_fn):
    """
    Return True if a video file can be read (basic integrity check)
    """
    import video
    is_verified = True
    try:
        video.info(video_fn)
    except Exception as _e:
        import traceback
        import sys
        print('>>>>>>>>Exception for video: {}\n{}<<<<<<<<'.format(
            video_fn,
            ''.join(traceback.format_exception(*sys.exc_info()))))
        is_verified = False
    return is_verified


def get_list_of_corrupted_sequences(infofile_json, recording_dir, verify_csv=True, num_workers=10):
    pool = util.Pool(num_workers)
    infofile_json = copy.deepcopy(infofile_json)
    infofile_json['basepath'] = recording_dir
    ifile = infofile_utils.AsaphusDataset(infofile_json)
    corrupted_sequences = []
    for seq in ifile.sequences:
        video_fn = ifile.get_video_for_sequence(seq)
        if verify_csv and not os.path.isfile(video_fn + '.csv'):
            corrupted_sequences.append(seq)
        else:
            pool.apply_async([seq], _verify_video_file, video_fn)
    for seq, is_verified in pool:
        if not is_verified:
            corrupted_sequences.append(seq)
    pool.wait_until_finished(False)
    return corrupted_sequences


def cleanup_sequences(updated_ifile, recording_dir, verify_video_integrity=True):
    '''Removes sequences from the infofile that for some reason are not referenced in the recorder infofile or whose
       video files are not readable.'''
    sequences_without_meta = [seq for seq, _meta in updated_ifile['sequences'].items()
                              if '_instructions' not in _meta]
    for seq in sequences_without_meta:
        del updated_ifile['sequences'][seq]

    if verify_video_integrity:
        corrupted_sequences = get_list_of_corrupted_sequences(updated_ifile, recording_dir)
        for seq in corrupted_sequences:
            del updated_ifile['sequences'][seq]


def fix_sequence_meta(json_data, recording_dir):
    '''fills in missing num_frames/rec_duration for the given dataset in case the recording session wasn't closed properly'''
    for sequence_id in json_data['sequences']:
        sequence = json_data['sequences'][sequence_id]
        if sequence.get('num_frames', None) is None or sequence.get('rec_duration', None) is None:  # rec_duration probably cannot be missing right now, keeping it just in case
            csv_path = os.path.join(recording_dir, json_data['sequences'][sequence_id]['sequence_meta']['video_path']) + '.csv'
            if os.path.isfile(csv_path):
                csv_info = util.get_sequence_meta_from_csv(csv_path)
                if csv_info['num_frames'] is not None:
                    sequence['sequence_meta']['num_frames'] = csv_info['num_frames']
                else:
                    print('Problem reading num_frames from csv: {}'.format(csv_path))
                if csv_info['rec_duration'] is not None:
                    sequence['sequence_meta']['rec_duration'] = csv_info['rec_duration']
                else:
                    print('Problem reading rec_duration from csv: {}'.format(csv_path))
            else:
                print('Missing file: {}'.format(csv_path))


def add_optitrack_calibration(json_data, recording_dir, verbose=True):
    opticalib = get_calib_from_opticalib(get_opticalib(recording_dir))
    json_data['calibration_table']['extrinsics']['optitrack'] = {key: opticalib[key] for key in ['R', 't']}
    json_data['calibration_table']['volumes']['optitrack'] = dict(driver=dict())
    json_data['calibration_table']['volumes']['optitrack']['driver'] = {key: opticalib[key]
                                                                        for key in ['center', 'extent']}
    json_data['calibration_table']['intrinsics']['optitrack'] = {key: opticalib[key]
                                                                 for key in ['cX', 'cY', 'fX', 'fY', 'k', 'p']}
    json_data['calibration_table']['forward_pose']['optitrack'] = opticalib['forwardPose']
    json_data['calibration_table']['extra']['optitrack'] = {}

    for video_fn in glob.glob(os.path.join(recording_dir, '*.avi')):
        if video_fn.endswith('corrected.avi'):
            continue
        if verbose:
            print('Processing: ' + video_fn)
        seq_name = os.path.splitext(os.path.basename(video_fn))[0]
        if seq_name not in json_data['sequences']:
            # sequence was removed earlier (in cleanup_sequences)
            continue
        keys = json_data['sequences'][seq_name]['calibration']['default'].keys()
        json_data['sequences'][seq_name]['calibration']['optitrack'] = {key: 'optitrack' for key in keys}


def add_video_info(json_data, recording_dir, verbose=True):
    '''augments the infofile with video_size and video_fps taken from video.info()'''
    import video
    for video_fn in glob.glob(os.path.join(recording_dir, '*.avi')):
        seq_name = os.path.splitext(os.path.basename(video_fn))[0]
        if seq_name not in json_data['sequences']:
            # sequence was removed earlier (in cleanup_sequences)
            continue
        try:
            video_info = video.info(video_fn)
        except Exception:
            if verbose:
                print('WARNING failed to get video.info for ' + video_fn)
            continue
        json_data['sequences'][seq_name]['sequence_meta']['video_size'] = video_info['video_size']
        json_data['sequences'][seq_name]['sequence_meta']['video_fps'] = video_info['video_fps']


def generate_json_infofile_from_recording_dir(recording_dir, write_infofile=True, basepath=None,
                                              verify_video_integrity=True, try_to_fix_sequence_meta=True,
                                              verbose=True, add_qa_status_unverified=False,
                                              skip_add_video_info=False, outpath=None):
    """
    Updates a json infofile from a recording dir by setting basepath, calibration_table and (optitrack)
    calibration per sequence.

    """
    print('Generating infofile for: {}'.format(os.path.basename(recording_dir)))

    json_data = utils.io.load_json(os.path.join(recording_dir, 'infofile.json'))

    if basepath:
        json_data['basepath'] = basepath
    else:
        json_data['basepath'] = recording_dir

    json_data['calibration_table'] = generate_calibration_table(json_data)
    if intrinsics not in json_data['calibration_table']:
        json_data['calibration_table']['intrinsics'] = dict()
    if os.path.isfile(os.path.join(recording_dir, 'opticalib.json')):
        add_optitrack_calibration(json_data, recording_dir, verbose)

    cleanup_sequences(json_data, recording_dir, verify_video_integrity)  # TODO: check whether this is still necessary. if yes: fix the root cause. finally: delete here
    if not skip_add_video_info:
        add_video_info(json_data, recording_dir)
    remove_video_file_size(json_data)
    if try_to_fix_sequence_meta:
        fix_sequence_meta(json_data, recording_dir)
    # close session if necessary
    if 'session' in json_data:
        del json_data['session']

    if add_qa_status_unverified:
        json_data['dataset_meta']['qa_status'] = 'unverified'

    if write_infofile:
        if outpath is None:
            ifile_path = os.path.join(configuration.get_asapy_path(), 'infofiles',
                                      json_data['dataset_meta']['dataset_id'] + '.json')
        else:
            utils.io.mkdirs(outpath)
            ifile_path = os.path.join(outpath, json_data['dataset_meta']['dataset_id'] + '.json')
        utils.io.save_json(ifile_path, json_data)

    return json_data


def remove_video_file_size(json_data):
    """Remove key video_file_size_bytes from all sequence_metas

    It only exists to verify the integrity of the video file after transferring it. For encrypted recordings,
    this number will be outdated once the infofile is on the server because it refers to the encrypted file, while
    the server stores the decrypted file.
    """
    for sequence_id, sequence in json_data['sequences'].items():
        if 'video_file_size_bytes' in sequence['sequence_meta']:
            del sequence['sequence_meta']['video_file_size_bytes']


def generate_calibration_table(json_data):
    calibration_table = dict(
        default_calibration=dict(extra='0', extrinsics='0', forward_pose='0', intrinsics='default', volumes='0'),
        extra={'0': {}},
        # intrinsics={  # infofile object reads intrinsics directly from intrinsics module now
        #     '0': intrinsics.get_intrinsics_dict(json_data['dataset_meta']['camera'])},
        extrinsics={
            '0': infofile_utils.DEFAULT_EXTRINSICS_AND_VOLUMES[
                json_data['dataset_meta']['camera_position']]['extrinsics']},
        volumes={
            '0': infofile_utils.DEFAULT_EXTRINSICS_AND_VOLUMES[
                json_data['dataset_meta']['camera_position']]['volumes']},
        forward_pose={
            '0': infofile_utils.DEFAULT_EXTRINSICS_AND_VOLUMES[
                json_data['dataset_meta']['camera_position']]['forward_pose']}
    )
    return calibration_table


if __name__ == '__main__':
    # generate_seatbelt_infofile(ds_dir, ds_dir)
    # for ds in [
    #         '20200729_267b0475_Authentication',
    #         '20200730_26fd4f00_Authentication',
    #         '20200730_386c5bdf_Authentication',
    #         '20200730_4fe33a00_Authentication',
    #         '20200730_b75f15da_Authentication',
    #         '20200731_2c114903_Authentication',
    #         '20200731_79d9c5e7_Authentication',
    #         '20200731_a93d4e1f_Authentication',
    #         '20200731_f2ef81e2_Authentication',
    #         '20200803_02d790a8_Authentication',
    #         '20200803_0ddda801_Authentication',
    #         '20200803_1e147322_Authentication',
    #         '20200803_38387f6d_Authentication',
    #         '20200803_4ef087a3_Authentication',
    #         '20200803_57faa22a_Authentication',
    #         '20200803_5b55fdfc_Authentication',
    #         '20200803_a8ced108_Authentication',
    #         '20200803_cc0f94bc_Authentication',
    #         '20200803_cf78b238_Authentication',
    #         '20200803_e0711095_Authentication',
    #         '20200803_faa0b439_Authentication',
    #         '20200804_184ffa2c_Authentication',
    #         '20200805_0f901633_Authentication',
    #         '20200806_04656a14_Authentication',
    #         '20200806_46cc9815_Authentication',
    #         '20200806_5de3894b_Authentication',
    #         '20200806_6a22721e_Authentication',
    #         '20200806_6c182f78_Authentication',
    #         '20200806_9e7c1e2f_Authentication',
    #         '20200806_df905c21_Authentication',
    #         '20200806_ef96a783_Authentication']:
    #     ifile = util.load_infofile(ds, cache=False)
    #     print(ds)
    #     print(ifile.get_all_entities())
    #     generate_json_infofile_from_recording_dir(util.load_infofile(ds).basepath)
    #     print(util.load_infofile(ds, cache=False).get_all_entities())
    #     print('')
    # for ds in [
    #         '20200810_ca69a7d3_Authentication',  # fixed ID on avdata
    #         '20200811_76d93d30_Authentication',  # fixed ID on avdata
    #         '20200825_20ad0780_Authentication',  # fixed ID on avdata
    #         '20200828_2d0a6344_Authentication',  # assigned missing ID on avdata
    #         '20200828_d2c69e08_Authentication',  # assigned missing ID on avdata
    #         '20200901_f18fc27e_Authentication']:  # fixed ID on avdata
    #     ifile = util.load_infofile(ds, cache=False)
    #     print(ds)
    #     print(ifile.get_all_entities())
    #     generate_json_infofile_from_recording_dir(util.load_infofile(ds).basepath)
    #     print(util.load_infofile(ds, cache=False).get_all_entities())
    pass
    generate_json_infofile_from_recording_dir(r'C:\_Recording\20210414_60a6589f_Generic')
