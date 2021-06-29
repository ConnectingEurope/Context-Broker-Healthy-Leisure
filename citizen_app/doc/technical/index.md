# Technical documentation

The technical documentation focuses in the technical aspects of the Context Broker Healthy Leisure citizen app, as well as it explains how to develop new features or how specific parts of the solution work.

## Content

- [Launch the application for development](#launch-the-application-for-development)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [Used technologies](#used-technologies)
- [Understanding the code](#understanding-the-code)
  - [How to change API URL](#how-to-change-api-url)

### Launch the application for development

To use the application, it is recommended to follow the [deployment manuals](../tutorials/index.md). However, to launch the application for development purposes, follow these instructions.

#### Prerequisites

- Android 10 (API 29)

#### Installation

1. Download de APK file from the following [link](../../code/apk).

2. Copy the APK file into your smartphone using the preferred method (USB cable, shared folder, etc.).

3. In the smartphone, click on the APK file.

4. Accept the installation and if a notice appears that the author is not known, click on the "follow anyway" button.

5. The application will be installed on the smartphone.

[Top](#technical-documentation)

### Used technologies

The following technologies have been used for the development and the deployment of the Context Broker Healthy Leisure Citizen app:

- [Kotlin](https://kotlinlang.org/)

[Top](#technical-documentation)

### Understanding the code

#### How to change API URL

The app gets the information from Context Broker Healthy Leisure web component. You need to indicate diferent endpoints in your API to ingest correctly the information in the citizen app.

At the beginning of the fragments you can see the variables that contain the API URL. Example:

```android
class BeachFragment : Fragment() {
    val client = OkHttpClient()
    var Levante : Beach = Beach()
    var Poniente : Beach = Beach()
    var urllevante = "http://your_api_url" //Copy here the API URL
    var urlPoniente = "http://your_api_url" //Copy here the API URL
```

You have to change the value of "your_api_url" for the direction in which you have your API. For example:

```android
class BeachFragment : Fragment() {
    val client = OkHttpClient()
    var Levante : Beach = Beach()
    var Poniente : Beach = Beach()
    var urllevante = "http://visitBenidormcity.com/levanteBeach"
    var urlPoniente = "http://visitBenidormcity.com/ponienteBeach"
```

The fragments that you have to change are:

- BeachFragment.kt
- BikeFragment.kt
- HomeFragment.kt
- StreetFragment.kt

You also have to change the following .kt files:

- MainActivity.kt
- MainMenu.kt

[Top](#technical-documentation)