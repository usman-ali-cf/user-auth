from django.core.mail import send_mail


def send_activation_email(first_name, last_name, username, email, date_joined):
    message = (
        ("Subject: Welcome to User Management - Account Activation\nDear {name}, Welcome to User Management! "
         "We are thrilled to have you as a new member of our community. Your registration is an important "
         "step towards discovering and enjoying all the features our platform has to offer.\nHere are a few "
         "key details about your account:\n Username: {username}\nEmail: {email}\nRegistration Date: ["
         "join_date]\n").
        format(
            name={first_name + " " + last_name},
            username={username},
            email={email},
            data_joined={date_joined}
        )
    )
    try:
        send_mail("User Registration", message, 'usman.ali.codefulcrum.com', [email])
    except Exception as error:
        print('Error! Error raise while sending email', error)
