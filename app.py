from flask import Flask, render_template, request
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import time
from plyer import notification


app = Flask(__name__)

def setup_driver():
    options = Options()
    # Uncomment the line below to run in headless mode
    # options.add_argument("--headless")
    driver = Chrome(options=options)
    return driver

def visit_website(driver, url):
    driver.get(url)

def clear_cookies(driver):
    driver.delete_all_cookies()


@app.route('/')
def main():
    return render_template('main.html')



@app.route('/cookie', methods=['POST'])
def index():
    try:
        driver = setup_driver()
        site_url = request.form['site_url']
        delay = int(request.form['delay'])
        closing = int(request.form['closing'])

        visit_website(driver, site_url)
        start_time = time.time()

        while (time.time() - start_time) < closing:
            clear_cookies(driver)
            notification.notify(
                title='Cookie Cleared',
                message='A cookie has been cleared.',
            )

            time.sleep(delay)
            visit_website(driver, site_url)

        driver.quit()

        return render_template('main.html')

    except Exception as e:
        error_message = "An error occurred: " + str(e)
        return render_template('error.html', error_message=error_message)

if __name__ == "__main__":
    app.run(host='localhost', port=5000)

