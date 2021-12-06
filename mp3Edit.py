import os
import eyed3
from eyed3.id3.frames import ImageFrame


def SetFrontCover(audio_file, cover_file):
    '''
    mp3ファイルにアルバムアート(フロント)を設定する

    Parameters
    ----------
    audio_file : string
        対象のオーディオファイル
    cover_file : string
        対象のカバーファイル
    '''
    _, ext = os.path.splitext(cover_file)
    mime_type = GetMIMETypeOfImage(ext)

    if mime_type is None:
        # 未対応のファイル形式
        return False

    audio = eyed3.load(audio_file)
    if audio.tag is None:
        audio.initTag()

    audio.tag.images.set(ImageFrame.FRONT_COVER, 
                        open(cover_file,'rb').read(),
                        mime_type)
    audio.tag.save(version=eyed3.id3.ID3_V2_3)
    return True


def GetMIMETypeOfImage(ext):
    if (ext == '.jpg') or (ext == '.jpeg'):
        return 'image/jpeg'
    elif ext == '.png':
        return 'image/png'
    else:
        return None


def GetExtensionOfImage(mime_type):
    if mime_type == 'image/png':
        return 'png'
    else:
        return 'jpg'


def OutputImages(audio_file):
    '''
    アルバムアートを画像として保存する

    Parameters
    ----------
    audio_file : string
        対象のオーディオファイル
    '''
    audio = eyed3.load(audio_file)
    if audio.tag is None: return

    # ファイルと同じ場所に出力するため拡張子削除
    name, _ = os.path.splitext(audio_file)
    
    for i, image in enumerate(audio.tag.images):
        if image is None:
            continue
        ext = GetExtensionOfImage(image.mime_type)
        output_file = f'{name}_cover_{i}.{ext}'
        with open(output_file, "wb") as img_file:
            img_file.write(image.image_data)


if __name__ == "__main__":
    audio_file = r'D:\User\NAKATSU\Music\にじさんじ\linklink\LINK・LINK.mp3'
    cover_file = r'D:\MMD\Projects\EffectTest\cover001.png'
    OutputImages(audio_file)
    SetFrontCover(audio_file, cover_file)