# Dogecoin_Musk
 This is not a financial advice, use with caution

## In this project, I used following techs:
- [Selenium/Webdriver] - Webscraping Yahoo finance
- [Tweepy] - API request to get twitter data
- [Google Vision] - API request to test images from twitter data(vs [AWS Rekognition] and local [TensorFlow])
- [Matplotlib] - Plot data
- [Chrome] - Web browser for webscraping, developer mode 
- [VS code] - awesome code editor


## Installation

Dogecoin_Musk requires several python libraries and plugins

```sh
pip3 install beautifulsoup4 selenium matplotlib requests tweepy google-cloud-vision
```

For webscraping, we need to download chromedriver

https://chromedriver.chromium.org/downloads

select the exact same version as your chrome has and put it in the same folder as main.py

## Credentials
1. twitter API

    In order to get twitter data through tweepy, we need to register developer account on https://developer.twitter.com/en. After account is established, register a new app within your account and get your "consumer_key", "consumer_secret", "access_token", "access_token_secret". Put those values inside secrets.json in the same folder as main.py, like follows:
    ```python
    {
    "consumer_key":"vr78----------------ClgJK1J1",
    "consumer_secret":"uvAaRJy1aI----------------kN7nRxlPmx4lT",
    "bear_token":"AAAAAAAAA---AAAAAAERZPwEAAAAAl13ywN---------------Ug",
    "access_token":"2935755--------------pwPSOc",
    "access_token_secret":"ErjaLtx3-------------62FO5udkov6X"
    }
    ```
    
2. Google Vision API

    Follow [this link] to set up google developer account. Once registered a service account, download the json key file into the same folder as main.py. The json file will look as follows:
    ```python
    {
      "type": "service_account",
      "project_id": "vi***oge",
      "private_key_id": "350b8f*******dd4d00d784c8",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqjU4FUCn....i8LQ3gF0qVD1sQlXuxe\n6PwI0huXQn6E6VxpAhMUPg==\n-----END PRIVATE KEY-----\n",
      "client_email": "dog**er@visi****-doge.iam.gserviceaccount.com",
      "client_id": "1005**********5887992",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/d******gserviceaccount.com"
    }
    ```
    The instruction also noted the best practice is to use environment variable in the current session.
    Powershell
    ```powershell
    $env:GOOGLE_APPLICATION_CREDENTIALS="C:\yourpath\service-account-file.json"
    ```
    
    Please not Google Vision API only allows 1,000 label creation api request for free. Use with frugality.
## Development
| Day | Progress |
| ------ | ------ |
| Monday | get historical dogecoin price data and visualize the data |
| Tuesday | get timestamp of Musk's dogecoin twitter through API call |
| Wednesday | Analyze pictures about Elon Musk's dogecoin tweets |
| Thursday | Overlay twitter timestamp on price chart |
| Friday | Presentation |
|Future | Auto buy and sell dogecoin on robinhood based on Musk's twitter |

## Output
<img src="https://github.com/sun624/Bitcoin_musk/blob/master/price.png?raw=true" alt="result" width="400"/>

## License

MIT


[//]: # 
   [Selenium/Webdriver]: <https://www.selenium.dev/documentation/en/webdriver/>
   [tweepy]: <https://www.tweepy.org/>
   [Google Vision]: <https://cloud.google.com/vision>
   [Matplotlib]: <https://matplotlib.org/>
   [Chrome]: <https://www.google.com/chrome/>
   [VS code]: <https://code.visualstudio.com/>
   [this link]: <https://cloud.google.com/vision/docs/setup>
   [AWS Rekognition]: <https://aws.amazon.com/rekognition>
   [TensorFlow]: <https://www.tensorflow.org/>
