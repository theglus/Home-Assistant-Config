# Home-Assistant-Config
Welcome to theglus's Home Assistant setup. I hope you find value in the projects and documentation I've been working on. I'll be continuting to update my documentaion in the coming weeks so stay tuned. 
## Table of Contents 
* [Hardware](#-hardware)
* [Software](#-software)
* [Devices](#-devices)
* [Lovelace Dashboards](#-lovelace-dashboards)
* [Automations](#-automations)
## 🔩 Hardware
* [Home Assistant Server](#home-assistant-server)
* [Network](#network)
### Home Assistant Server
My Home Assistant setup is pretty basic but it gets the job done without any hiccups.
| [Raspberry Pi 4 Model B 4GB](https://a.co/d/1OWca61) | [Raspbee II](https://a.co/d/9k93ZNW) | [SanDisk Extreme 64GB MicroSD]https://a.co/d/6piTlaW) | [Argon Neo Case](https://a.co/d/73W0bTn) |
| --- | --- | --- | --- |
| ![Raspberry Pi 4 Model B 4GB](www/readme/ha_hardware/pi_4.jpg) | ![Raspbee II](www/readme/ha_hardware/raspbee_II.jpg) | ![SanDisk Extreme 64GB MicroSD](www/readme/ha_hardware/sandisk_64.jpg) | ![Argon Neo Pi case](www/readme/ha_hardware/argon_neo.jpg) |

I opted to go the Zigbee route primarily because I really like the Aqara platform. I landed on the Raspbee II over the Conbee as it just seemed like a more elegant solution. It's a little bit of a pain to initially setup, but after that it's smooth sailing. 
### Network
Living in a 950 sqft Loft apartment, I don't have to worry about signal strength. My setup consists of a Google WiFi puck in the Living Room. This is my primary router: one end connects to my in-wall ethernet port and the other end to a TP-Link 8-port network switch. 
| [Google Wifi](https://store.google.com/us/product/google_wifi_2nd_gen?hl=en-US) | [TP-Link Switch](https://a.co/d/3TJbImA) | [MoCa Network Adapter](https://a.co/d/fYFKBw5) |
| --- | --- | --- |
| ![Google Wifi](www/readme/network/google_wifi.jpg) | ![TP-Link Switch](www/readme/network/switch.jpg) | ![MoCa Network Adapter](www/readme/network/coax.jpg) |

But you can't have a mesh network with just one puck, so in order to eliminate the potential for any deadzones, I've placed another puck upstairs in the Loft.

I routinely stream games via Moonlight from my desktop computer (in the Office) to the TV (in the Living Room). Initially, I did this over WiFi, but had very little success. Fortunately, there is a coax outlet right under my desk, so using ethernet-over-coax, I am able to hardwire to the network switch in the Living Room.

## 💾 Software
* [Architecture](#architecture)
* [Integrations](#integrations)
* [Custom Components](#custom-components) 
* [Lovelace Resources](#lovelace-resources)
* [Voice Assistant](#voice-assistant) 
### Architecture
![My Home Assistant Architecture](www/readme/architecture.png) 
### Integrations
<details>
  <summary>See details</summary>
 
- [Air Visual](https://www.home-assistant.io/integrations/airvisual)
- [ClimaCell](https://www.home-assistant.io/integrations/climacell)
- [deCONZ](https://www.home-assistant.io/integrations/deconz)
- [Denon AVR Network Receiver](https://www.home-assistant.io/integrations/denonavr)
- [Denon HEOS](https://www.home-assistant.io/integrations/heos)
- [DLNA](https://www.home-assistant.io/integrations/dlna_dmr)
- [Google Cast](https://www.home-assistant.io/integrations/cast)
- [Mobile App](https://www.home-assistant.io/integrations/mobile_app)
- [MQTT](https://www.home-assistant.io/integrations/mqtt)
- [Nanoleaf](https://www.home-assistant.io/integrations/nanoleaf)
- [Philips Hue](https://www.home-assistant.io/integrations/hue)
- [Sony Bravia TV](https://www.home-assistant.io/integrations/braviatv)
- [Tile](https://www.home-assistant.io/integrations/tile)
- [TP-Link Kasa Smart](https://www.home-assistant.io/integrations/tplink)
- [Xiaomi Miio](https://www.home-assistant.io/integrations/xiaomi_miio)
 
</details>


### Custom Components
<details>
  <summary>See details</summary>
 
- [HACS](https://github.com/hacs/integration): Allows for the installation and management of the various custom components.
- [BrowserMod](https://github.com/thomasloven/hass-browser_mod): Supports various customizations within Home Assistant.
- [Coway IoCare](https://github.com/RobertD502/home-assistant-iocare): Adds support for Coway Airmega to HA.
- [Drivvo Integration](https://github.com/theglus/sensor.drivvo): Utilized to pull in Vespa milage + fuel economy from [Drivvo](https://github.com/theglus/sensor.drivvo).
- [Dyson Local/Cloud](https://github.com/shenxn/ha-dyson): Add support for Dyson air purifiers to HA.
- [Frigidaire](https://github.com/bm1549/home-assistant-frigidaire): Adds support for Frigidaire portable AC to HA. This is what originally got me interested in Home Assistant. Ironically I wasn't able to get it working until a year in.
- [Google Home](https://github.com/leikoilja/ha-google-home): Creates HA sensors for alarms + timers that have been set on various Google Home devices.
- [LG ThinQ Sensors](https://github.com/ollo69/ha-smartthinq-sensors): Supports integrating my LG washer + dryer into HA.
- [PowerCalc](https://github.com/bramstroker/homeassistant-powercalc): Virtual power sensors for estimated tracking of energy consumption.
- [TrueNAS](https://github.com/tomaae/homeassistant-truenas): Adds the ability to monitor and control my TrueNAS Scale NAS directly in HA.
- [Xiaomi Cloud Map Extractor](https://github.com/PiotrMachowski/Home-Assistant-custom-components-Xiaomi-Cloud-Map-Extractor): Harnesses lidar in RoboRock S4 to create a live map of my home.
 
</details>
 
### Lovelace Resources
<details>
  <summary>See details</summary>
 
- [Bar Card](https://github.com/custom-cards/bar-card)
- [Button Card](https://github.com/custom-cards/button-card)
- [Card Mod](https://github.com/thomasloven/lovelace-card-mod)
- [Declutter Card](https://github.com/custom-cards/decluttering-card)
- [Home Assistant Swipe Navigation](https://github.com/zanna-37/hass-swipe-navigation)
- [Home Assistant Swipe Navigation](https://github.com/zanna-37/hass-swipe-navigation)
- [Hue Icon](https://github.com/arallsopp/hass-hue-icons)
- [Hui Element](https://github.com/thomasloven/lovelace-hui-element)
- [Layout Card](https://github.com/thomasloven/lovelace-layout-card)
- [Light Popup Card](https://github.com/DBuit/light-popup-card)
- [Lovelace Xiaomi Vacuum Map card](https://github.com/PiotrMachowski/lovelace-xiaomi-vacuum-map-card)
- [Media Player Popup Card](https://github.com/DBuit/media_player-popup-card)
- [Mini Graph Card](https://github.com/kalkih/mini-graph-card)
- [RGB Light Card](https://github.com/bokub/rgb-light-card)
- [Paper Button Rows](https://github.com/jcwillox/lovelace-paper-buttons-row)
- [Sidebar Card](https://github.com/DBuit/sidebar-card)
- [Simple Thermostat](https://github.com/nervetattoo/simple-thermostat)
- [Slider Entity Row](https://github.com/thomasloven/lovelace-slider-entity-row)
- [Stack in Card](https://github.com/custom-cards/stack-in-card)
- [State Switch](https://github.com/thomasloven/lovelace-state-switch)
- [Switch Popup Card](https://github.com/DBuit/switch-popup-card)
- [Thermostat Popup Card](https://github.com/DBuit/thermostat-popup-card)
- [Vertical Stack in Card](https://github.com/ofekashery/vertical-stack-in-card)
 
</details> 

### Voice Assistant
I'm currently utilizing Nabu Casa to leverage Google Assistant via the aforementioned Google Home devices to enable voice controls. I mainly use voice commands to trigger the lights, music, and theater system. I would like to setup voice commands for Winston and Kirby in the near future. 
## 🕹 Devices
* [Audio & Video](#audio--video)
  * [Home Theater](#home-theater)
  * [Multi Room Audio](#multi-room-audio)
* [Appliances](#appliances)
  * [Climate](#climate)
  * [Vacuum](#vacuum)
  * [Lighting](#lighting)
  * [Switches + Outlets](#switches--outlets)
  * [Laundry](#laundry)
### Audio & Video
#### Home Theater
I recently built out my home theater system centered around my Denon S960H + NVIDIA SHIELD TV Pro and managed by Home Assistant using `denonavr`, `androidtv`, and `media_player`. The system is primarly controlled using the NVIDIA SHIELD Toblerone as it can accomplish almost everything I need via CEC. The main gaps currently in the system are the following Denon buttons `Setup`, `Options`, `Info`, `Back`, `ECO`, `Input` and the following Sony Bravia buttons `Settings`, `Home`. I'm working to create a series of `custom:button-cards` and 
`media_player-popup-cards` to control my Home Theater with the ultimate goal of eliminating the need for all remotes but the Tobelerone. 
| [Denon 960H](https://www.bhphotovideo.com/c/product/1571155-REG/denon_avrs960h_7_2_channel_home_theatre.html) | [Polk S35](https://www.bhphotovideo.com/c/product/1342730-REG/polk_audio_s35_center_channel_multi_purpose_home.html) | [Polk S10](https://www.bhphotovideo.com/c/product/1342734-REG/polk_audio_s10_two_way_surround_speaker.html) | [Polk S50](https://www.bhphotovideo.com/c/product/1342729-REG/polk_audio_s50_small_two_way_floor.html) | [NVIDIA SHIELD TV Pro](https://a.co/d/2xHjdVf) | [Sony TV](https://a.co/d/9dySjA0) |
| --- | --- | --- | --- | --- | --- |
| ![Denon](www/readme/av/denon.png) | ![Polk S35](www/readme/av/polk_s35.jpg) | ![Polk S10](www/readme/av/polk_s10.jpg) | ![Polk S50](www/readme/av/polk_s50.jpg) | ![NVIDIA SHIELD TV Pro](www/readme/av/nvidia_shield_tv_pro.jpg) | ![Sony](www/readme/av/sony_x900h.jpg) |

I have a Levovo Smart Tab M8 that is docked in my living room that I use to access my _[Lovelace Dashboards](#lovelace-dashboards)_ including my Home Theater controls in Home Assistant. 
#### Multi Room Audio + Displays
I have a series of Google Home and Nest Mini's scattered throughout the apartment for the purpose of multi-room audio. The audio quality is subpar, but it gets the job done for now. I'm planning on updating to several pairs of Google Nest Audio smart speakers.
| [Google Nest Mini](https://store.google.com/us/product/google_nest_mini?hl=en-US) | [Google Nest Audio](https://store.google.com/us/product/nest_audio?hl=en-US) | Google Nest Hub | [Lenovo Smart Clock](https://www.lenovo.com/gb/en/smart-clock/) | [Lenovo M8 Smart Tablet](https://www.lenovo.com/us/en/p/tablets/android-tablets/lenovo-tab-series/smart-tab-m8-google-assistant/len103l0006) |
| --- | --- | --- | --- | --- |
| ![Google Home Mini](www/readme/av/google_mini.jpg) | ![Google Nest Audio](www/readme/av/nest_audio.jpg) | ![Google Nest Hub](www/readme/av/google_nest_hub.jpg) | ![Lenovo Smart Clock](www/readme/av/lenovo_smart_clock.jpg) | ![Lenovo M8 Smart Tablet](www/readme/av/lenovo_m8.jpg) |

The Google Nest Hub lives in the loft and is used as a control panel, picture frame, and alarm clock. The Lenovo Smart Clock lives in the downstairs bedroom (referred to in HA as Office) for use as an alarm clock and simplified control panel.
### Appliances
| [Dyson Pure Cool Purifying Fan TP04](https://www.dyson.com/air-treatment/purifiers/dyson-pure-cool/dyson-pure-cool-tower-white-silver) | [Frigidaire Cool Connect Portable AC FGPC1244T1](https://a.co/d/i7ARVG2) | [Airmega 400S Air Purifier](https://a.co/d/9VWsrRB) | [Roborock S4 Robot Vacuum](https://a.co/d/07T35Dz) | [LG Smart Washer WM3900HBA](https://www.lg.com/us/washers/lg-WM3900HBA-front-load-washer) | [LG Smart Dryer DLEX3900B](https://www.lg.com/us/dryers/lg-DLEX3900B-electric-dryer) |
| --- | --- | --- | --- | --- | --- |
| ![Dyson TP04](www/readme/appliance/dyson_tp04.jpg) | ![Frigidaire](www/readme/appliance/frigidaire.jpg) | ![Airmega 400S Air Purifier](https://home-assistant-readme.s3.amazonaws.com/appliances/airmega.jpg) | ![Roborock](www/readme/appliance/roborock.jpg) | ![LG Smart Washer](www/readme/appliance/washer.jpg) | ![LG Smart Dryer](www/readme/appliance/dryer.jpg) |
#### Climate
My climate situation is pretty simple, just a fan and portable AC. The Dyson air purifying fan (Kirby) lives in the loft and is WiFi enabled. Shortly after purchase I realized it lacked the ability to integrate with Google Assistant, this became a huge driver in me exploring Home Assistant. I was pleasantly surprised to learn it contains a `temperature`, `humidity`, `aqi`, and `dust` sesnor. I successfully integrated Kirby with Home Assistant and am utilizing the `tempurature` and `humidity` sensors in my Lovelace dashboard. The [Climate Kirby](includes/automations/climate_kirby.yaml) automation was created to allow me to stop using the Dyson app for various scheduling functionality.

My apartment has casement windows so my AC options were fairly limited. The Frigidaire Cool Connect Portable AC (Ice Bear) was an easy decision due to it's high BTUs, small footprint, and WiFi conductivity. Unfortunately the smart functionality is incredibly limited and the Frigidaire app very slow to load, making less than ideal for controlling the unit. Thanks to [bm1549](https://github.com/bm1549) I was able to use the [Fridigaire custom component](https://github.com/bm1549/home-assistant-frigidaire) to integrate Ice Bear with Home Assistant. This was a HUGE development as it means I can control the AC via Google Assistant as well.
#### Vacuum
The first floor of my apartment is serviced by a [Roborock S4](https://a.co/d/07T35Dz) named Winston. The Roborock S4 intrigued me due to it's lidar, smart mapping, and friendliness with Home Assistant. A lot of people report that you have to do a crazy hack switching the region in Mainland China, but I didn't have to do that, you can read more about my process/HA vacuum implimentation in the wiki under [WINSTON my Roborock S4](https://github.com/theglus/Home-Assistant-Config/wiki/WINSTON-my-Roborock-S4).
#### Lighting
I'm pretty deep into the Hue ecosystem sans my Sengled lightstrip. As a result I have my lights paired directly to the Hue app using the Hue bridge. The main reason I did this instead of utilizing my Raspbee II was so I can ensure my lights remain functional regardless of if Home Assistant is operational. This allows me a lot more flexibility to work with Home Assistant without adversely effecting the other people in my household. 
| [Hue Starter Kit](https://a.co/d/cqyZFPy) | [BR30 White Ambiance](https://a.co/d/25pj5jB) | [Hue Color](https://a.co/d/i7HmDXJ) | [Sengled Light Strip](https://a.co/d/aVl0VMJ) |
| --- | --- | --- | --- |
| ![Hue Starter Kit](www/readme/lighting/hue_starter.jpg) | ![BR30 White Ambiance](www/readme/lighting/hue_br30.jpg) | ![Hue Color](www/readme/lighting/hue_color.jpeg) | ![Sengled Light Strip](www/readme/lighting/sengled_ledstrip.jpg) |

The only light outside the Hue ecosystem is my Sengled LED strip. I needed 6 feet of LEDs just for my stairs not to mention the other areas of the apartment, it would have been $79 for 6.5' of Hue lights where Sengled was ~$60 for 16.5'. The LED strip is hooked up directly to the Raspbee II. 
#### Switches + Outlets
I have a series of smart plugs which I use to control various appliances. I recently migrated from Kasa HS103 outlets to Sengled plugs in order the strengthen my Zigbee network. Additionally, the Sengled plugs have engergy monitoring capabilities.
| [Hue Smart Plug](https://a.co/d/cRt5O9x) | [Sengled Energy Monitoring Plugs](https://a.co/d/3luPeQJ) | [Kasa 3-plug Surge](https://a.co/d/fe35mXo) | [Lutron Aurora](https://a.co/d/c9uJlks) | 
| --- | --- | --- | --- |
| ![Hue Smart Plug](www/readme/switches/hue_plug.jpg) | ![Sengled Energy Monitoring Plugs](https://home-assistant-readme.s3.amazonaws.com/switches/sengled_plug.jpg) | ![Kasa Surge](www/readme/switches/kasa_surge.jpg) | ![Lutron Aurora](www/readme/switches/lutron_aurora.jpg) |

My old school analog marquee is controlled by the Hue plug which I opted for due to it's ability to be integrated with my other lights via the Hue ecosystem. Lastly, sometimes it's just quicker and quieter to turn on the lights with a switch, being a renter replacing my wall switches isn't appealing. Luckily I discovered Lutron Aurora dimmers which not only gives me a physical button but also a dimmer which I can map to one or many lights. I'm hoping to figure out a way to map secondary actions (double click, triple click, etc.), but the feasiblity is TBD.
## Custom Icons
Inspired by [matt8707](https://github.com/matt8707), I created several custom icons which can be found in `www/custom_icons.js`. I leveraged [material design principles](https://material.io/design/iconography/system-icons.html#design-principles) and [Guide to a Vector Drawing Program](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/XML.html) when designing and building the icons. I will be working on pulling in additional icons from various [icon_templates](includes/lovelace/button_card_templates/icon_templates) over the next several weeks.
## 🎛 Lovelace Dashboards
* [Quick Access Controls](#quick-access-controls)
  * [Room Controls](#room-controls)
  * [Hallway Controls](#hallway-controls)
  * [Laundry Controls](#laundry-controls)
  * [Office Controls](#office-controls)
  * [Living Room Controls](#living-room-controls)
  * [Kitchen Controls](#kitchen-controls)
  * [Loft Controls](#loft-controls)
* [Popup Controls](#popup-controls)
  * [Light Popup](#light-popup)
  * [Animated Icons](#animated-icons)
* [Vacuum Dasboard](#vacuum-dashboard)
* [System Dashboard](#system-dashboard)
### Quick Access Controls
The Quick Access Controls are a logical grouping of Lovelace buttons + cards using many of the [above listed custom components](#custom-components). The inspiration for Quick Access came from stumbling upon [Crixle's Light Control Card](https://github.com/crixle/homeassistant-config#light-control-card) via r/homeassistant. I was fascinated by the idea of reducing the number of clicks required to control my smart home. This led me to overhaul my Lovelace setup with the goal of making all essential controls availible in 3-clicks or less.

[Quick Access Controls](https://user-images.githubusercontent.com/2943783/231850800-9f004212-5fc7-4fd3-af17-6edbd818e389.webm) 
<details>
  <summary>Code</summary>
  
```
## Toggle Nav
entities:
  - type: "custom:paper-buttons-row"
    buttons:
## General Button
      - entity: input_select.lighttoggle
        name: false
        icon: "mdi:home-assistant"
        state_styles:
          General:
          template: nav_button
        template: nav_styles
        tap_action:
          action: call-service
          service: input_select.select_option
          service_data:
            entity_id: input_select.lighttoggle
            option: General
## Entryway Button
      - entity: input_select.lighttoggle
        name: false
        icon: "mdi:coat-rack"
        state_styles:
          Entrway:
          template: nav_button
        template: nav_styles
        tap_action:
          action: call-service
          service: input_select.select_option
          service_data:
            entity_id: input_select.lighttoggle
            option: Entryway
## Expanded
- type: "custom:state-switch"
  entity: input_select.lighttoggle
  default: Entryway
  transition: none
  states:
## General Controls
  General:
    type: "custom:mod-card"
    style: |
      ha-card { 
        background: rgba(0,0,0,.3); 
        padding: 10px; 
        border-radius: 35px; 
        margin-top: none; 
        }
    card:
      type: grid
      columns: 3
      cards:

    ## <--- Buttons --->
  
## Entryway Controls
  General:
    type: "custom:mod-card"
    style: |
      ha-card { 
        background: rgba(0,0,0,.3); 
        padding: 10px; 
        border-radius: 35px; 
        margin-top: none; 
        }
    card:
      type: grid
      columns: 3
      cards:

    ## <--- Buttons --->
```
</details>

### Room Controls

![Room Controls](https://home-assistant-readme.s3.amazonaws.com/room_controls.png)
#### Icons
- [Entryway Icon](www/custom_icons.js)
- [Office Icon](www/custom_icons.js)
- [Living Room Icon](www/custom_icons.js)
- [Kitchen Icon](www/custom_icons.js)
- [Loft Icon](www/custom_icons.js)

<details>
  <summary>Code</summary>
  
```
## General Controls
General:
  type: "custom:mod-card"
  style: |
    ha-card { 
      background: rgba(0,0,0,.3); 
      padding: 10px; 
      border-radius: 35px; 
      margin-top: none; 
      }
  card:
    type: grid
    columns: 3
    cards:
## Weather button
      - type: "custom:button-card"
        custom_fields:
          s2: |
            [[[
              return states['sensor.aqi'].state + ' AQI'
            ]]]
        entity: weather.loft
        label: |
          [[[
            return states['weather.climacell_nowcast'].attributes.temperature + '°F '
          ]]]
        name: |
          [[[
            return "Next hour " + states['weather.climacell_hourly'].attributes.forecast[1].temperature + '°F'
          ]]]
        template:
          - weather_layout
          - weather
          - icon_weather
        triggers_update:
          - sun.sun
## Entryway button
      - type: "custom:decluttering-card"
        template: declutter_room_button
        variables:
          - room: Entryway
          - light: light.group_hallway
          - sensor: binary_sensor.front_door
          - message_on: Door is open
          - message_off: Door is closed
          - icon_state: mdi:door-open
          - icon_default: custom:room-hallway
## Office button
      - type: "custom:decluttering-card"
        template: declutter_room_button
        variables:
          - room: Office
          - light: light.overhead
          - sensor: sensor.major_laser_printer
          - message_on: Printer on
          - message_off: Printer off
          - icon_state: mdi:printer
          - icon_default: custom:room-office
## Living Room button
      - type: "custom:decluttering-card"
        template: declutter_temp_button
        variables:
          - light: light.group_living_room
          - hvac: switch.switchbot
          - sensor_temp: sensor.temperature_living_room
          - message_on: Heat is on
          - message_off: Heat is off
          - icon_state: mdi:radiator
          - icon_default: custom:room-living
          - room: Living Room
## Kitchen button
      - type: "custom:decluttering-card"
        template: declutter_temp_button
        variables:
          - light: light.group_kitchen
          - hvac: fan.kitchen
          - sensor_temp: sensor.kitchen_temperature
          - message_on: Dyson is on
          - message_off: Dyson is off
          - icon_state: custom:room-kitchen
          - icon_default: custom:room-kitchen
          - room: Kitchen
## Loft button
      - type: "custom:decluttering-card"
        template: declutter_temp_button
        variables:
          - light: light.loft
          - hvac: fan.kirby
          - sensor_temp: sensor.kirby_temperature
          - message_on: Dyson is on
          - message_off: Dyson is off
          - icon_state: custom:room-loft
          - icon_default: custom:room-loft
          - room: Loft
```
</details>

### Hallway Controls

![Hallway Controls](https://home-assistant-readme.s3.amazonaws.com/hallway.png)
#### Icons
- [Marquee Icon](includes/lovelace/button_card_templates/icon_templates/icon_light/icon_marquee.yaml)
- [Stair Icon](includes/lovelace/button_card_templates/icon_templates/icon_light/icon_led.yaml)
- [Lamp Icon](includes/lovelace/button_card_templates/icon_templates/icon_light/icon_lamp.yaml)
- [Spotlight Icon](includes/lovelace/button_card_templates/icon_templates/icon_light/icon_spot.yaml)
- [Door Icon](includes/lovelace/button_card_templates/icon_templates/icon_door.yaml)
- [Smart Clock Icon](includes/lovelace/button_card_templates/icon_templates/icon_media/icon_smart_clock.yaml)

<details>
  <summary>Code</summary>
  
```
## Entrway Controls
Entryway:
  type: "custom:mod-card"
  style: |
    ha-card { 
      background: rgba(0,0,0,.3); 
      padding: 10px; 
      border-radius: 35px; 
      margin-top: none; 
      }
  card:
    type: grid
    columns: 3
    cards:
## Hallway Marquee
      - type: "custom:button-card"
        entity: light.hallway_marquee
        template:
          - icon_marquee
## Hallway Runner
      - type: "custom:button-card"
        entity: light.hallway_runner
        name: Runner
        template: 
          - icon_led
## Potter Lamp
      - type: "custom:button-card"
        entity: light.potter_lamp
        name: Lamp
        template:
          - light_color
          - icon_lamp
## Stair Light
      - type: "custom:button-card"
        entity: light.stair
        name: Lamp
        template:
          - light
          - icon_spot
## Front Door Sensor
      - type: "custom:button-card"
        entity: binary_sensor.front_door
        template: 
          - icon_door
## Hallway Smart Clock
      - type: custom:button-card
        entity: media_player.smart_clock
        name: Smart Clock
        template:
          - icon_smart_clock
```
</details>

### Laundry Controls

![Laundry Controls](https://home-assistant-readme.s3.amazonaws.com/laundry.png) 
#### Icons
- [Washer Icon](includes/lovelace/button_card_templates/icon_templates/icon_laundry/icon_washer.yaml)
- [Dryer Icon](includes/lovelace/button_card_templates/icon_templates/icon_laundry/icon_dryer.yaml)
<details>
  <summary>Code</summary>
  
```
## Guest Bathroom Controls
Laundry:
  type: "custom:mod-card"
  style: |
    ha-card { 
      background: rgba(0,0,0,.3); 
      padding: 10px; 
      border-radius: 35px; 
      margin-top: none; 
      }
  card:
    type: grid
    columns: 3
    cards:
## Washer
      - type: "custom:button-card"
        entity: sensor.washer
        name: Washer
        template:
          - icon_washer
## Dryer
      - type: "custom:button-card"
        entity: sensor.dryer
        name: Dryer
        template:
          - icon_dryer
```
</details>

### Office Controls

![Office Controls](https://home-assistant-readme.s3.amazonaws.com/office.png) 
#### Icons
- [Ceiling Icon](includes/lovelace/button_card_templates/icon_templates/icon_light/icon_recessed.yaml)
- [Printer Icon](includes/lovelace/button_card_templates/icon_templates/icon_printer.yaml)
- [Air Circulator Icon](includes/lovelace/button_card_templates/icon_templates/icon_climate/icon_circulator.yaml)
- [Google Nest Mini Icon](includes/lovelace/button_card_templates/icon_templates/icon_media/icon_nest_mini.yaml)
<details>
  <summary>Code</summary>
  
```
## Office Controls
Office:
  type: "custom:mod-card"
  style: |
    ha-card { 
      background: rgba(0,0,0,.3); 
      padding: 10px; 
      border-radius: 35px; 
      margin-top: none; 
      }
  card:
    type: grid
    columns: 3
    cards:
## Office Overhead Lights
      - type: "custom:button-card"
        entity: light.overhead
        name: Ceiling
        template:
          - light
          - icon_recessed
## Printer
      - type: "custom:button-card"
        entity: switch.major_laser_printer
        name: Major Laser
        template: 
          - icon_printer
## Air Circulator
      - type: "custom:button-card"
        entity: switch.kettle
        name: Air Circulator
        template:
          - icon_circulator
## Office Google Home Mini
      - type: custom:button-card
        entity: media_player.office_speaker
        name: Home Mini
        template:
          - icon_nest_mini
```
</details>

### Living Room Controls

![Living Room Controls](https://home-assistant-readme.s3.amazonaws.com/living_room.png)
#### Icons
- [Spotlight Icon](includes/lovelace/button_card_templates/icon_templates/icon_light/icon_spot.yaml)
- [Garden Lights Icon](includes/lovelace/button_card_templates/icon_templates/icon_light/icon_garden.yaml)
- [Lamp Icon](includes/lovelace/button_card_templates/icon_templates/icon_light/icon_lamp.yaml)
- [Heater Icon](includes/lovelace/button_card_templates/icon_templates/icon_climate/icon_heater.yaml)
- [Air Circulator Icon](includes/lovelace/button_card_templates/icon_templates/icon_climate/icon_circulator.yaml) 
- [AC Icon](includes/lovelace/button_card_templates/icon_templates/icon_climate/icon_ac.yaml)
- [TV Icon](includes/lovelace/button_card_templates/icon_templates/icon_media/icon_tv.yaml)
<details>
  <summary>Code</summary>
  
```
## Living Room Controls
Living Room:
  type: "custom:mod-card"
  style: |
    ha-card { 
      background: rgba(0,0,0,.3); 
      padding: 10px; 
      border-radius: 35px; 
      margin-top: none; 
      }
  card:
    type: grid
    columns: 3
    cards:
## Track Light
      - type: "custom:button-card"
        entity: light.track
        name: Track
        template:
          - light_color
          - icon_spot
## Garden Light
      - type: "custom:button-card"
        entity: light.garden
        name: Garden
        template: 
          - icon_garden
## Yumi Lamp
      - type: "custom:button-card"
        entity: light.yumi_lamp
        name: Lamp
        template:
          - light_color
          - icon_lamp
## Heater
      - type: "custom:button-card"
        entity: switch.switchbot
        template:
          - icon_heater
## Living Room Air Circulator
      - type: "custom:button-card"
        entity: switch.air_circulator
        name: Air Circulator
        template:
          - icon_circulator
## Ice Bear
      - type: "custom:button-card"
        entity: climate.ice_bear
        name: Air Conditioner
        double_tap_action:
          action: more-info                  
        template:
          - icon_ac
        variables:
          circle_input: >
            [[[
              return entity === undefined ?
                null :
                entity.attributes.temperature;
            ]]]
## Shield
      - type: "custom:button-card"
        entity: media_player.shield_tv
        tap_action:
          action: toggle
        template:
          - icon_tv
```
</details>

### Kitchen Controls

![Kitchen Controls](https://home-assistant-readme.s3.amazonaws.com/kitchen.png) 
#### Icons
- [Spotlight Icon](includes/lovelace/button_card_templates/icon_templates/icon_light/icon_spot.yaml)
- [Nanoleaf Icon](includes/lovelace/button_card_templates/icon_templates/icon_light/icon_dinopanel.yaml)
- [Google Nest Mini Icon](/Users/Glusman/Home-Assistant-Config/includes/lovelace/button_card_templates/icon_templates/icon_media/icon_nest_mini.yaml)
- [Dyson Icon](includes/lovelace/button_card_templates/icon_templates/icon_media/icon_dyson.yaml)

<details>
  <summary>Code</summary>
  
```
## Kitchen Controls
Kitchen:
  type: "custom:mod-card"
  style: |
    ha-card { 
      background: rgba(0,0,0,.3); 
      padding: 10px; 
      border-radius: 35px; 
      margin-top: none; 
      }
  card:
    type: grid
    columns: 3
    cards:
## Kitchen Track
      - type: "custom:button-card"
        entity: light.kitchen
        name: Track
        template:
          - light_color
          - icon_spot
## Nanoleaf Dino Panesl
      - type: "custom:button-card"
        entity: light.nanoleaf
        template: 
          - icon_dinopanel
## Kitchen Google Home Mini
      - type: custom:button-card
        entity: media_player.living_room_speaker
        name: Home Mini
        template:
          - icon_nest_mini
## Kitchen Dyson
      - type: "custom:button-card"
        entity: fan.kitchen
        name: Dyson
        template:
          - icon_dyson
```
</details>

### Loft Controls

![Loft Controls](https://home-assistant-readme.s3.amazonaws.com/loft.png) 
#### Icons
- [Bedside Icon](includes/lovelace/button_card_templates/icon_templates/icon_light/icon_bed.yaml)
- [Table Lamp Icon](includes/lovelace/button_card_templates/icon_templates/icon_light/icon_bedside.yaml)
- [Spotlight Icon](includes/lovelace/button_card_templates/icon_templates/icon_light/icon_spot.yaml)
- [Lamp Icon](includes/lovelace/button_card_templates/icon_templates/icon_light/icon_lamp.yaml)
- [Dyson Icon](includes/lovelace/button_card_templates/icon_templates/icon_climate/icon_dyson.yaml)
- [Nest Hub Mini Icon](includes/lovelace/button_card_templates/icon_templates/icon_media/icon_nest_hub.yaml)

<details>
  <summary>Code</summary>
  
```
## Loft Controls
Loft:
  type: "custom:mod-card"
  style: |
    ha-card { 
      background: rgba(0,0,0,.3); 
      padding: 10px; 
      border-radius: 35px; 
      margin-top: none; 
      }
  card:
    type: grid
    columns: 3
    cards:
      ## Bedside Lights
      - type: "custom:button-card"
        entity: light.bedside
        name: Bedside
        template: 
          - icon_bedside
## His Light
      - type: "custom:button-card"
        entity: light.jeffreys_lamp
        name: Jeffrey's
        template: 
          - icon_bed
## Her Light
      - type: "custom:button-card"
        entity: light.tiffanys_lamp
        name: Tiffany's
        template: 
          - icon_bed
## Bed Track
      - type: "custom:button-card"
        entity: light.loft_bed_light
        name: Ceiling
        template:
          - light
          - icon_spot
## Desk Lights
      - type: "custom:button-card"
        entity: light.loft_desk_lamp
        name: Desk
        template:
          - light
          - icon_lamp
## Dyson
      - type: "custom:button-card"
        entity: fan.kirby
        name: Dyson
        template:
          - icon_dyson
## Loft Nest Hub
      - type: custom:button-card
        entity: media_player.loft_nest_hub
        name: Nest Hub
        template:
          - icon_nest_hub    
```
</details>

## 🤖 Automations
### 🌡 Climate
Before Home Assistant, I had several schedules setup for my two air purifiers in the Dyson App. I was able to easily replace those with two automations in HA, eliminating my need to use the proprietary Dyston App. My air circulators which are hooked up to Kasa smart plugs, utilitze two of my favorite automations. One turns on the downstairs fan when the tempurature in the Loft is ≥72° and off when ≤71°, the other turns the office fan on/off based on the state of the lights in the room.
<details>
  <summary>Automations</summary>

- [Climate Kirby](includes/automations/climate_kirby.yaml): Trigger [Kirby: Daytime](includes/scenes/kirby_daymode.yaml) @ 8 am + [Kirby: Nighttime](includes/scenes/kirby_nightmode.yaml) @ 9 pm.
- [Climate Loft](includes/automations/climate_loft.yaml): Turn on fan when Loft is ≥72° and off when ≤71°.
- [Climate Office Off](includes/automations/climate_office_off.yaml): Turn fan OFF based off of Overhead light group.
- [Climate Office On](includes/automations/climate_office_on.yaml): Turn fan ON based off of Overhead light group.
</details>

### 🎚 Dimmer
Lutton Aurora dimmers have been a game changer in my home automations setup. They are natively supported by Philips Hue and as a renter, they are the perfect solution as to mount onto the existing light switch. Not all my lights are in the Hue ecosystem, so I've created automations to allow the dimmers to control my Sengled LED light strip and various Kasa smart plugs.
<details>
  <summary>Automations</summary>

- [Dimmer Hallway](includes/automations/dimmer_hallway.yaml): Trigger runner light with Lutron Aurora switch.
- [Dimmer Office](includes/automations/dimmer_office.yaml): Trigger office lights with Lutron Aurora switch.
</details>

### 📬  Notifications
I currently have notifications set to be delivered via one of two channels [Telegram](includes/notifiers/telegram.yaml) or the [Smartphone Group](includes/notifiers/smartphones.yaml). Telegram is used to notify about server boot up to aid with troubleshooting while the Smartphone Group leverages the companion app to surface in-app notifications.
<details>
  <summary>Automations</summary>

- [Notify AQI](includes/automations/notify_aqi.yaml): Notify Smartphones when AQI is >75.
- [Notify Dryer](includes/automations/notify_dryer.yaml): Notify smartphones when dryer is complete.
- [Notify Heat Wave](includes/automations/notify_heatwave.yaml): Notify smartphones when tomorrows high is  >75 °F.
- [Notify Printer](includes/automations/notification_printer.yaml): Notify Smartphones when Major Laser Printer is ready.
- [Notify Washer](includes/automations/notify_washer.yaml): Notify smartphones when washer is complete.
- [Peak Usage Alerts](includes/automations/peak_usage_alerts.yaml): Notify Smartphones when AC, Washer, or Dryer is on during peak usage. 
- [Server Boot Up](includes/automations/server_boot_up.yaml): Notify via Telegram when server has booted up.
- [Server Reboot](includes/automations/server_reboot.yaml): Telegram notification that alerts of server reboot, restart, or shutdown.
</details>

### 🚪 Presence
I decided to take a unique approach to presence automations and forgo the use of motion sensors, in favor of manual triggers before leaving the apartment. I have an [Aqara Mini Switch](https://a.co/d/eQp5jyT) next to the door, which triggers automations based on the number of button clicks and status of the front door sensor.
<details>
  <summary>Automations</summary>

- [Leave Home](includes/automations/leave_home.yaml): Notify smartphones of door status + turn off lights accordingly.
- [Leave Vacuum](includes/automations/leave_vacuum.yaml): Notify smartphones of door status + turn off lights + vacuum.

</details>

### 🔌 Shutoff
Vampire drain is a problem, especially when your power company charges different rates depending on the time of day. There are a lot of devices thats only need to be powered briefly to do their job. My printer + paper shredder are setup to turn-off after a set period of time, limiting their idle power usage to minutes instead of hours or days.
<details>
  <summary>Automations</summary>

- [Charge Toothbrushes](includes/automations/charge_toothbrushes.yaml): Start charging toothbrushes at 12 am and stop at 4 am.
- [Printer Shutoff](includes/automations/shutoff_printer.yaml): Shutoff plug to printer 15-minutes after device has been switched on.
- [Shutdown Shredder](includes/automations/shutoff_shredder.yaml): Shutoff plug to paper shredder 2-minutes after device has been switched on.
</details>

### 🧹 Vacuum
Winston my trusty robot vacuum is scheduled to clean the most trafficed areas of my apartment (hallway + kitchen) Monday - Friday, the remaining rooms (office + living room + bathroom) are cleaned on Tuesdays and Thursdays. Creating these automations allowed me to stop using the [Mi Home App](https://play.google.com/store/apps/details?id=com.xiaomi.smarthome&hl=en_US&gl=US).
<details>
  <summary>Automations</summary>

- [Select Vacuum Speed](includes/automations/select_vacuum_speed.yaml): Adds vacuum.set_fan_speed service calls to Vacuum Speed Helper.
- [Vacuum Clean](includes/automations/vacuum_clean.yaml): Notify Smartphones when Winston starts cleaning.
- [Vacuum Docked](includes/automations/vacuum_done.yaml): Notify Smartphones when Winston has returned to dock.
- [Vacuum Done](includes/automations/vacuum_done.yaml): Notify Smartphones when Winston has completed cleaning.
- [Vacuum Schedule](includes/automations/vacuum_schedule.yaml): Clean hallway + kitchen @ 10:30 pm M - F & clean bathroom + office + living room @ 10:30 pm T and TH.
</details>

### 🎰 Various
The remaining automations are super useful, but don't fit into any specific category. This includes alerts for water leaks, scheduled volume controls for Google Home devices, and an `on air` light to indicate when a video call is in progress.
<details>
  <summary>Automations</summary>

- [Alert Leak](includes/automations/alert_leak.yaml): Alert when water is detected under the sink or dishwasher.
- [Mood Television](includes/automations/mood_television.yaml): Television scene + Denon Nighttime quick select.
- [Mood Theater](includes/automations/mood_theater.yaml): Theater scene + Denon Theater quick select.
- [Office Available](includes/automations/office_available.yaml): Turn Potter light magenta when webcam turns off.
- [Office Busy](includes/automations/office_busy.yaml): Turn Potter light red when webcam turns on.
- [Set Theme](includes/automations/set_theme.yaml): Set theme at Home Assistant start.
- [Volume Home](includes/automations/volume_home.yaml): Turn down volume of Google Home device at 10 pm.
</details>

# 📢 Shoutouts and Inspirition
If you like my Lovelace setup be sure to checkout those who influenced me:

**[crixle](https://github.com/crixle/homeassistant-config)**
 
I was racking my brain as to how I could reducing the number of clicks required to control my smart home. A Reddit post with crixle's [Light Control Card](https://github.com/crixle/homeassistant-config#light-control-card) inspired me to create my [Quick Access Controls](#quick-access-controls).
  
**[eximo84](https://github.com/eximo84/homeassistant-config-v2)**
 
The [Room Controls](#room-controls) buttons leverage code from eximo84's [Weather](https://github.com/eximo84/homeassistant-config-v2/blob/master/Custom%20Buttons/Weather%20Button.yaml) and [Light](https://github.com/eximo84/homeassistant-config-v2/blob/master/Custom%20Buttons/Light%20Button.yaml) buttons.
 
**[matt8707](https://github.com/matt8707/hass-config)**
 
The original inspiration for overauling my Lovelace dashboard was kicked-off when I stumbled upon [A different take on designing a Lovelace UI](https://community.home-assistant.io/t/a-different-take-on-designing-a-lovelace-ui/162594).

My approach to button templates was heavily influence by Matt's [button_card_templates.yaml](https://github.com/matt8707/hass-config/blob/master/button_card_templates.yaml). His approach to custom icons also inspired me to learn how to create SVGs in Inkspace and SVGator. Matt's work gave me the push to move towards a 100% `yaml` approach to my Lovelace dashboard and greatly increased my all around technical knowledge.

# 👋
Thanks for reading, please star if your are interested in the project.
