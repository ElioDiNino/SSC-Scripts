CWL = "example"
PASSWORD = "password"
EMAIL_LIST = ["example1@domain.com", "example2@domain.com "]
# By default, UBC Webmail has a long delay before it sends an email so make sure this delay is long enough
# that the email sends before the browser is closed.
EMAIL_SEND_DELAY = 60
CHECK_INTERVAL = 3600  # 1 hour
# Choose whether the data found on the script runner's SSC will be included in the email.
# Disable this if you are emailing multiple people and you want to keep your grades/specialization private.
SEND_DATA = False
