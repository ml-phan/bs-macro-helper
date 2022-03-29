import os
import video
import utils.io


def write_interpolated_frame(video_fn, interpolate):
    reader = video.reader(video_fn, interpolate_rgbir=interpolate)
    frame = reader.__next__()
    print('Writing frame: {}'.format(frame.shape))
    img_fn = '{}__{}.png'.format(os.path.splitext(video_fn)[0],
                                 'interp' if interpolate else 'nointerp')
    utils.io.imwrite(img_fn, frame)


video_file = r"Y:\_TEMP\_Phan\20220316_faf408ba_Reference_120Wide_A_015\A015_with_light.avi"
# write_interpolated_frame(video_file, False)
write_interpolated_frame(video_file, True)
write_interpolated_frame(video_file, False)
