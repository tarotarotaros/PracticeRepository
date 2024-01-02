import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


class GoogleDriveFacade:

    # 設定値
    SETTING_PATH = './Settings/settings.yaml'
    # Google Drive URLの基本部分
    BASE_DRIVE_URL = 'https://drive.google.com/uc?id='

    # コンストラクタ
    def __init__(self):
        gauth = GoogleAuth(self.SETTING_PATH)
        gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(gauth)

    # フォルダ作成
    def create_folder(self, folder_name):
        ret = self.check_files(folder_name)
        if ret:
            folder = ret
            print(f"{folder['title']}: exists")
        else:   
            folder = self.drive.CreateFile(
                {
                    'title': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
            )
            folder.Upload()

        return folder

    # 存在チェック：存在する場合は先頭
    def check_files(self, folder_name,):
        query = f'title = "{os.path.basename(folder_name)}"'

        list = self.drive.ListFile({'q': query}).GetList()
        if len(list)> 0:
            return list[0]
        return False

    # アップロード実行
    def upload(self, 
               local_file_path: str,
               save_folder_name: str ,
               is_convert : bool=True,
        ):
        
        if save_folder_name:
            folder = self.create_folder(save_folder_name)
        
        file = self.drive.CreateFile(
            {
                'title':os.path.basename(local_file_path),
                'parents': [
                    {'id': folder["id"]}
                ]
            }
        )
        file.SetContentFile(local_file_path)
        file.Upload({'convert': is_convert})
        
        drive_url = f"{self.BASE_DRIVE_URL}{str( file['id'] )}" 
        return drive_url
    
        
if __name__ == "__main__":
    g = GoogleDriveFacade()
    g.upload(
        local_file_path='hoge.txt',
        save_folder_name="Backup",
        is_convert=True,
    )
