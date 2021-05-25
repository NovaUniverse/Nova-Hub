# Nova-Hub
<p align="center">
 <img src="https://user-images.githubusercontent.com/66202304/119562923-d15dcd00-bd9e-11eb-8653-589393a2b3bc.png" width="300" height="300" />
</p>

### Nova Hub is an app that players can use to rapidly install Mod Packs for game modes like Terra Smp so they don't have to worry about finding all the mods and downloading forge.
#### The app also allows for automatic modpack updates, viewing news from the Nova Universe feed, managing the minecraft clients/modpacks and even more features that will be added in the future.


* What all the files do.
  * settings.py - Where you can make changes to the app like example the url to take the user to if he clicks on the nova universe logo.
  * nova_hub.py - This python file is bascally the ring around the app.py. It's what checks for Nova Hub updates; manages them and also repairs the app if there's any missing files.
  * app.py - This is the gui app itself. This is usually ran by the nova_hub.py file.
  * nova_func - This is where I store all the globally used functions for the purpose of keeping the code neat in general.
