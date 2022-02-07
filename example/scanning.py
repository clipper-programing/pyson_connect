import pyson_connect

def main(email):
    pc = pyson_connect.PysonConnect()

    #認証
    auth = pc.authentification(email)
    access_token = auth["access_token"]
    refresh_token = auth["refresh_token"]
    subject_id = auth["subject_id"]
    print(auth)

    #スキャン宛先一覧の取得
    dest = pc.get_scan_destination_list()
    print(dest)

    #スキャン宛先登録
    alias_name = input("Type 'alias_name': ")
    dest_type = input("Type 'mail' or 'url': ")
    destination = input("Type 'emailAddress' or 'webAddress': ")
    destData = {
            "alias_name":alias_name,
            "dest_type":dest_type,
            "destination":destination
            }
    pc.register_scan_destination(destData)

    dest = pc.get_scan_destination_list()
    print(dest)

    #スキャン宛先変更
    print("update destinations")
    alias_name = input("Type 'alias_name': ")
    dest_type = input("Type 'mail' or 'url': ")
    destination = input("Type 'emailAddress' or 'webAddress': ")
    scan_dest_id = input("Type 'scan_dest_id': ")
    updateData = {
            "scan_dest_id":scan_dest_id,
            "alias_name":alias_name,
            "dest_type":dest_type,
            "destination":destination,
            }
    pc.update_scan_destination(updateData)

    dest = pc.get_scan_destination_list()
    print(dest)

    #スキャン宛先削除
    scan_dest_id = input("If you want delete destination. Type 'scan_dest_id': ")
    if scan_dest_id != "":
        pc.delete_scan_destination(access_token, subject_id, scan_dest_id)

    dest = pc.get_scan_destination_list()
    print(dest)

    #認証取り消し
    pc.cancel_authentication(access_token, subject_id)

if __name__ == "__main__":
    email = input("email: ")
    main(email)
