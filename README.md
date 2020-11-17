# Home-Assistant-Config
Home Assistant Configuration &amp; Documentation for my Smart House.
## Devices + services used with Home Assistant
## Audio & Video
I recently built out my home theater system centered around my Denon S960H + NVIDIA SHIELD TV Pro and managed by Home Assistant using `denonavr`, `androidtv`, and `media_player`. The system is primarly controlled using the NVIDIA SHIELD Toblerone as it can accomplish almost everything I need via CEC. The main gaps currently in the system are the following Denon buttons `Setup`, `Options`, `Info`, `Back`, `ECO`, `Input` and the following Sony Bravia buttons `Settings`, `Home`. I currently have a _Home Theater_ Lovelace view which I use to control powering one or many entities (TV, AV, Shield) as well as switching between `AUTO` and `SETTING` Denon sound modes. 
| Denon 960H | Polk S35 | Polk S10 | Polk S15 | NVIDIA SHIELD TV Pro | Sony TV |
| --- | --- | --- | --- | --- | --- |
| ![Denon](img/av/denon.png) | ![Polk S35](img/av/polk_s35.jpg) | ![Polk S10](img/av/polk_s10.jpg) | ![Polk S15](img/av/polk_s15.jpg) | ![NVIDIA SHIELD TV Pro](img/av/nvidia_shield_tv_pro.jpg) | ![Sony](img/av/sony_x900h.jpg) |

I have a Levovo Smart Tab M8 that is docked in my living room that I use to access the _Home Theater_ view in Home Assistant. This view is very much a WIP progress and is my focus over the coming weeks.
# Home Automation Components
## Home Assistant Hardware
| Raspberry Pi 4 Model B 4GB | Raspbee II | SanDisk Extreme 64GB MicroSD | Argon Neo Case |
| --- | --- | --- | --- |
| ![Raspberry Pi 4 Model B 4GB](img/ha_hardware/pi_4.jpg) | ![Raspbee II](img/ha_hardware/raspbee_II.jpg) | ![SanDisk Extreme 64GB MicroSD](img/ha_hardware/sandisk_64.jpg) | ![Argon Neo Pi case](img/ha_hardware/argon_neo.jpg) |
## Home Assistant Software + Architecture
![My Home Assistant Architecture](architecture.png) 
## Voice Assistant
WIP
## Lighting
WIP
## Security
WIP
## Plugs
WIP
 * To-dos
   * See git issues
---
## Depricating
### Devices + services used with Home Assistant
 * Hubs
   * Hue Bridge
   * Raspbee II
 * Lights + Switches
   * Hue bulbs
   * Hue plug
   * Lutron Aurora
   * Sengled LED strip
   * TP Link Kasa plugs 
 * Media
   * Sony Bravia
   * Denon AVR-S960H
   * NVIDIA Shield Pro
 * Notifications
   * Telegram
 * Sensors
   * Aqara door sensor
   * Aqara water sensors
 * Voice Integrations
   * Google Home with Nabu Casa 
 * Weather + Climate
   * Dyson
