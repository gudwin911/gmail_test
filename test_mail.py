from Page import LogInPage
import pytest


@pytest.mark.parametrize("mail,password,mail_subject,mail_txt",
                         [("chekount@gmail.com", "greatpass123$", "Subject", "Hello World!")])
def test_check_email_text(driver, mail, password, mail_subject, mail_txt):
    email = LogInPage(driver).\
        log_in(mail, password).\
        create_new_mail(mail, mail_subject, mail_txt).\
        wait_for_email(mail). \
        get_mail_data()
    assert email == (mail_subject, mail_txt)


if __name__ == "__main__":
    pytest.main()
