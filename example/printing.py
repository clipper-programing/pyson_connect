import pyson_connect


class printer:
    def __init__(self, epson_email):
        self.pc = pyson_connect.PysonConnect()
        # 認証関数の実行
        auth = self.pc.authentification(epson_email)


    def settings(self, setting_data):
        # 印刷設定関数の実行
        settings = self.pc.print_setting(setting_data)


    def file_upload(self, file_path, document_type):
        # ファイルアップロード関数の実行
        self.pc.upload_print_file(file_path, document_type)


    def printing(self):
        # 印刷実行関数の実行
        self.pc.excute_print()


if __name__ == "__main__":
    email = input("input EpsonConnect Email: ")
    p = printer(email)
    # 印刷タイプ
    # ドキュメントを印刷する場合:document
    # 写真を印刷する場合:photo
    document_type = input("input document_type(document/photo): ")
    # 印刷設定(この場合はEpson Connectが定義したデフォルト設定で印刷される。)
    # 用紙の設定や給紙トレイの場所の指定、カラーやモノクロなどの詳しい指定方法はライブラリのドキュメントを参照。
    p.settings({"job_name":"demo", "print_mode":document_type})
    # 印刷したいファイルをアップロード
    file_path = input("input filePath: ")
    p.file_upload(file_path, document_type)
    # 印刷実行
    p.printing()
