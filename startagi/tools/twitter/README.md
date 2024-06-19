<p align="center">
<a href="https://startagi.khulnasoft.com//#gh-light-mode-only">
<img src="https://startagi.khulnasoft.com/wp-content/uploads/2023/05/Logo-dark.svg" width="318px" alt="StartAGI logo" />
</a>
<a href="https://startagi.khulnasoft.com//#gh-dark-mode-only">
<img src="https://startagi.khulnasoft.com/wp-content/uploads/2023/05/Logo-light.svg" width="318px" alt="StartAGI logo" />
</a>
</p>

# StartAGI Twitter Toolkit

Introducing Twitter Toolkit for StartAGI. With Twitter Integrated into StartAGI, you can now deploy agents to

1. Send Tweets
2. Send Tweets with Images

## Installation

### 🛠️ Setting up StartAGI:

Set up StartAGI by following the instructions given [here](https://github.com/KhulnaSoft/StartAGI/blob/main/README.MD)

### 🔐 Obtaining API Key and Secret from Twitter Developer Portal

1. Log in to your Twitter Developer Portal Account and select your project under the “Projects & Apps” section.

![TW1](https://github.com/KhulnaSoft/StartAGI/assets/133874957/7ee7be42-2e20-4b44-beee-92b754031967)
  
2. Proceed with creating a new app. Once you have created the app by adding a name, you will get an API Key and an API Secret, copy that and keep it in a separate text file.

![TW2](https://github.com/KhulnaSoft/StartAGI/assets/133874957/4d0d91ec-d22c-4027-b472-d1bc1c692ac7)
![TW3](https://github.com/KhulnaSoft/StartAGI/assets/133874957/caf265e7-60ac-4a5e-be8b-4b2b9d0fdd15)


### 🚪 Configuring OAuth

3. Once you have saved the key and the secret, click on “App Settings”
4. Once you are on the App Settings Page, start setting up the User Authentication Settings. 

![TW4](https://github.com/KhulnaSoft/StartAGI/assets/133874957/5db07a1e-3104-4a83-8de8-2394d41268ca)

5. Fill in the details as shown in the below image. Give “Read and Write Permissions” and make it a “Web Application"
    
![TW5](https://github.com/KhulnaSoft/StartAGI/assets/133874957/08d322f3-b248-49e6-8e5c-85f8d84b9a5f)
    
6. Add the Callback URI and the Website URL as shown in the image below

![TW_OAUTH_URI](https://github.com/Phoenix2809/StartAGI/assets/133874957/66c555f5-0546-4961-acbd-acd393c52ecf)

7. Save the settings. you have now configured OAuth Authentication for Twitter.

 ### ✅ Configuring Keys and Authenticating in StartAGI.

1. In the StartAGI’s Dashboard, navigate to the Twitter Toolkit Page, add the API Key and API Secret you’ve saved, and click on ‘Update Changes’

![TW7](https://github.com/KhulnaSoft/StartAGI/assets/133874957/cab23842-e515-495a-b697-14587d832abc)

2. After you’ve updated the changes, click on Authenticate. This will take you to the OAuth Flow. Authorize the app through the flow. 

![TW8](https://github.com/KhulnaSoft/StartAGI/assets/133874957/62f877ac-dc1f-475d-9c5c-52040a197762)

Once you have followed the above steps, you have successfully integrated Twitter with StartAGI. 
