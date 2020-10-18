# PanoptoSync

An automated way to download lecture videos from Panopto.

## Usage

This has been designed to work with macOS LaunchAgents. All the configuration items have been abstracted out to environment variables (detailed below). After configuring it, stick the plist file into your `~/Library/LaunchAgents` and load it.

You will also need to enable the Folder Watch extension within jDownloader. Configure it to the `PANOPTOSYNC_CRAWLJOB_FOLDER` you'll set below. It's best to enable Silent Mode in the global jDownloader settings.

## Environment Variables

* **PANOPTOSYNC_SSO_URL**
  - Your university's SSO login URL. Tested to work with Apereo CAS.
  - Example: `https://sso.university.edu/cas/login?service=https%3A%2F%2Funiversity.instructure.com%2Flogin%2Fcas`

* **PANOPTOSYNC_SSO_USERNAME**
  - Your university username.

* **PANOPTOSYNC_SSO_PASSWORD**
  - Your university password.

* **PANOPTOSYNC_PANOPTO_DOMAIN**
  - Your university's Panopto instance domain.
  - Example: `university.hosted.panopto.com`
  
* **PANOPTOSYNC_DOWNLOAD_FOLDER**
  - The parent folder that will contain your final videos, organized by class subfolders.
  - Example: `/path/to/download/folder/`
  
* **PANOPTOSYNC_CRAWLJOB_FOLDER**
  - The folder you've configred your jDownloader Folder Watch extension to monitor.
  - Example: `/path/to/jdownloader/monitored/folder/`
  
* **PANOPTOSYNC_[CLASS]_FEED**
  - The RSS feed for your class's videos. Check out the class specific Python files and `sync.py` for guidance on customizing this to your specific classes.
  - Example: `university.hosted.panopto.com`
  
## LaunchAgent Config

* **StartInterval**
  - The time to wait in seconds between script runs.
  - Example: `600` is 10 minutes.
