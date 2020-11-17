# Home-Assistant-Config
Home Assistant Configuration &amp; Documentation for my Smart House.
# Audio & Video
## Home Theater
I recently built out my home theater system centered around my Denon S960H + NVIDIA SHIELD TV Pro and managed by Home Assistant using `denonavr`, `androidtv`, and `media_player`. The system is primarly controlled using the NVIDIA SHIELD Toblerone as it can accomplish almost everything I need via CEC. The main gaps currently in the system are the following Denon buttons `Setup`, `Options`, `Info`, `Back`, `ECO`, `Input` and the following Sony Bravia buttons `Settings`, `Home`. I currently have a _Home Theater_ Lovelace view which I use to control powering one or many entities (TV, AV, Shield) as well as switching between `AUTO` and `SETTING` Denon sound modes. 
| Denon 960H | Polk S35 | Polk S10 | Polk S15 | NVIDIA SHIELD TV Pro | Sony TV |
| --- | --- | --- | --- | --- | --- |
| ![Denon](img/av/denon.png) | ![Polk S35](img/av/polk_s35.jpg) | ![Polk S10](img/av/polk_s10.jpg) | ![Polk S15](img/av/polk_s15.jpg) | ![NVIDIA SHIELD TV Pro](img/av/nvidia_shield_tv_pro.jpg) | ![Sony](img/av/sony_x900h.jpg) |

I have a Levovo Smart Tab M8 that is docked in my living room that I use to access the _Home Theater_ view in Home Assistant. This view is very much a WIP progress and is my focus over the coming weeks.
## Multi Room Audio
I have a series of Google Home and Nest Mini's scattered throughout the apartment for the purpose of multi-room audio. The audio quality is subpar, but it gets the job done for now. I eventually plan on augmenting the audio with several Denon Home speakers.
| Google Home/Nest Mini | Google Nest Hub | Lenovo Smart Clock |
| --- | --- | --- | 
| ![Google Home Mini](img/av/google_mini.jpg) | ![Google Nest Hub](img/av/google_nest_hub.jpg) | ![Lenovo Smart Clock](img/av/lenovo_smart_clock.jpg) |

The Google Nest Hub lives in the loft and is used as a control panel, picture frame, and alarm clock. The Lenovo Smart Clock lives in the downstairs bedroom (referred to in HA as Office) for use as an alarm clock and simplified control panel.
# Appliances
| Dyson Pure Cool Purifying Fan TP04 | Frigidaire Cool Connect Portable AC FGPC1244T1 | Roborock S4 Robot Vacuum |
| --- | --- | --- |
| ![Dyson TP04](img/appliance/dyson_tp04.jpg) | ![Frigidaire](img/appliance/frigidaire.jpg) | ![Roborock](img/appliance/roborock.jpg) |
## Climate
My climate situation is pretty simple, just a fan and portable AC. The Dyson air purifying fan (Kirby) lives in the loft and is WiFi enabled. Shortly after purchase I realized it lacked the ability to integrate with Google Assistant, this became a huge driver in me exploring Home Assistant. I was pleasantly surprised to learn it contains a `temperature`, `humidity`, `aqi`, and `dust` sesnor. I successfully integrated Kirby with Home Assistant and am utilizing the `tempurature` and `humidity` sensors in my Lovelace dashboard. 
I have plans to create a comprehensive fan/purifier control card as a keystone for my climate view in HA.
My apartment has casement windows so my AC options were fairly limited. The Frigidaire Cool Connect Portable AC (Ice Bear) was an easy decision due to it's high BTUs, small footprint, and WiFi conductivity. Unfortunately the smart functionality is incredibly limited and the Frigidaire app is complete garabage. I have yet to figure out a strategy to get Ice Bear into Home Assistant, but haven't given up hope!
## Vacuum
I recently replaced my Eufy robovac due to it's tendency to try to kill itself by ramming into various objects. The Roborock S4 (Winston) intrigued me due to it's lidar, smart mapping, and friendliness with Home Assistant. A lot of people report that you have to do a crazy hack switching the region in Mainland China, but I didn't have to do that, you can read more about my process/HA vacuum implimentation in the wiki under [Project WINSTON](https://github.com/theglus/Home-Assistant-Config/wiki/Project-WINSTON:-Roborock-S4).

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
| Hue Starter Kit | BR30 White Ambiance | Hue Color | Sengled Light Strip |
| --- | --- | --- | --- |
| ![Hue Starter Kit](img/lighting/hue_starter.jpg) | ![BR30 White Ambiance](img/lighting/hue_br30.jpg) | ![Hue Color](img/lighting/hue_color.jpeg) | ![Sengled Light Strip](img/lighting/sengled_ledstrip.jpg) |
## Security
WIP
## Plugs
WIP
