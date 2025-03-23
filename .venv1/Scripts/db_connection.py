from itsdangerous import URLSafeSerializer
import pandas as pd
import sqlite3


class Db:
    def __init__(self):
        self.data_base = sqlite3.connect("users_data.db")
        self.cursor = self.data_base.cursor()
        self.__safe_serializer = URLSafeSerializer('secret-key')
        self._logins = []

    def import_from_default_xlsx_file_to_database(self):
        users_data = pd.read_excel(
            'C:/Users/adria/PycharmProjects/Kwintesencjozator_ambarasu_3000/.venv/data/users.xlsx',
            sheet_name="full_data")  # login/password/rights

        try:
            is_remembered = pd.read_excel(
                'C:/Users/adria/PycharmProjects/Kwintesencjozator_ambarasu_3000/.venv/data/users.xlsx',
                sheet_name="is_remembered_per_user")  # login/remember_me_value
        except ValueError:
            is_remembered = None

        for index in range(len(users_data)):
            self._logins = users_data["Login"]
            usernames = users_data['Login']
            passwords = users_data['Password']
            rights = users_data['Power']

            self.cursor.execute(f"""INSERT INTO users_login_and_pass (username, password) 
                                VALUES (?, ?)"""
                                , (usernames.iloc[index], passwords.iloc[index]))

            self.cursor.execute("""INSERT INTO users_rights (username, rights) 
                                VALUES (?, ?)
                                """, (usernames.iloc[index], rights.iloc[index])
                                )

        for index in range(len(is_remembered)):
            usernames = is_remembered['Login']
            is_remembered = is_remembered['remember_me_value']

            self.cursor.execute("""INSERT INTO remember_me_value_per_username (username, is_remembered)
                                VALUES (?, ?)""", (usernames.iloc[index], is_remembered.iloc[index])
                                )

        self.data_base.commit()

    @property
    def logins(self) -> list[str]:
        for tuple_of_usernames in self.cursor.execute("""SELECT username FROM users_login_and_pass""").fetchall():
            for username in tuple_of_usernames:
                if username not in self._logins:
                    self._logins.append(username)

        self.data_base.commit()
        return self._logins

    @logins.setter
    def logins(self, new_value):
        self.logins = new_value

    @logins.deleter
    def logins(self):
        del self.logins

    def _get_password(self, username: str) -> str:
        dumped_passw = self.__safe_serializer.dumps(self.cursor.execute("""SELECT password 
                                                                        FROM users_login_and_pass 
                                                                        WHERE username == ?""",
                                                                        (username,)).fetchone()[0]
                                                    )
        self.data_base.commit()
        return dumped_passw

    def _set_password(self, new_password) -> None:
        pass

    def _del_password(self) -> None:
        pass

    def _get_rights(self, login: str):
        this_user_rights_tuple = self.cursor.execute("""SELECT rights from users_rights WHERE username == ?""", (login)).fetchone()
        self.data_base.commit()
        return this_user_rights_tuple[0]

    def _set_rights(self):
        pass

    def _del_rights(self):
        pass

    def _get_safe_serializer(self) -> URLSafeSerializer:
        return self.__safe_serializer

    def _get_remembered(self):
        username = self.cursor.execute(
            """SELECT username FROM remember_me_value_per_username WHERE is_remembered == 1""").fetchone()
        self.data_base.commit()
        return username

    def _update_users_data_file(self, remember_me_data: int, username: str) -> None:
        self.cursor.execute("""INSERT INTO remember_me_value_per_username (username, is_remembered) 
                            VALUES (?, ?)""", (username, remember_me_data))
        self.data_base.commit()

    def _login_validation(self, login_value: str) -> [str, bool]:
        if login_value in self.logins:
            return login_value

        else:
            return False

    def _password_validation(self, login_validation_output_value: str, password_entry_value: str) -> bool:
        if not login_validation_output_value:
            return False

        if password_entry_value == self._get_password(login_validation_output_value):
            return True

        else:
            return False

    def _login_processing(self, root_object) -> bool:
        login_entry_value = root_object.login_frame_utilities.login_entry.get()
        password_entry_value = self._get_safe_serializer().dumps(root_object.login_frame_utilities.password_entry.get())
        remember_me_checkbox_value = root_object.login_frame_utilities.remember_me_checkbox_variable.get()

        login_validation_result = self._login_validation(login_entry_value)

        if not login_validation_result:
            root_object.clear_entries(which_entry=root_object.login_frame_utilities.login_entry)
            root_object.login_frame_utilities.login_process_execution_label.configure(text=f"Wrong login! Try again.")
            return False
        else:
            password_validation_result = self._password_validation(login_validation_result, password_entry_value)

        if remember_me_checkbox_value and password_validation_result:
            remember_me_data = 1
            self._update_users_data_file(remember_me_data, login_entry_value)

        if password_validation_result:
            root_object.logged_in_screen_process()
            return True
        else:
            Counter.password_entry()
            root_object.login_frame_utilities.login_process_execution_label.configure(text=f"Wrong password! Try again.")
            root_object.clear_entries(which_entry=root_object.login_frame_utilities.password_entry)

        if Counter.password_entry_counter % 3 == 0 and Counter.password_entry_counter > 0:
            root_object.freeze_login_processors()
            return False


class Counter:
    password_entry_counter = 1

    @classmethod
    def password_entry(cls):
        cls.password_entry_counter += 1
