# Angelix ICSE'16 experiments #

This repository contains [Angelix](https://github.com/mechtaev/angelix) ICSE'16 experimental results and scripts. Specifically, it includes repairs generated for the subjects of GenProg ICSE'12 benchmark and the Heartbleed vulnerability.

## Installation ##

Angelix experimental results are distrubuted in source code form and pre-installed form in VirtualBox image.

### Option 1: VirtualBox image ###

You can [request](https://docs.google.com/forms/d/1XoQ3AomEwd2hke7-ty8CDaQ_iH7TH3W5foO5BQWc-6o/viewform?usp=send_form) VirtualBox image with preinstalled Angelix and ICSE'16 evaluation scripts.

### Option 2: Build from source ###

Install Angelix following the instructions [here](https://github.com/mechtaev/angelix).

Install additional Wireshark dependencies:

    sudo apt-get install libffi-dev gtk-doc-tools libgtk2.0-dev libpcap-dev

Clone this repository.

## Evaluation ##

To generate a repair, execute `repair` script specifying subject and version. For example,

    ./repair libtiff d13be72c-ccadf48a
    
The full list of available versions is given below.

Experimental results such as patches and execution logs are available in the `patches` and `logs` directories accordingly. Note that your results may differ from the data in this repository. This is because Angelix relies on KLEE and Z3, that are both non-deterministic tools and their performance can depend on the used hardware.

## Repairs ##

* wireshark
  * 37112-37111
  * 37172-37171
  * 37172-37173
  * 37284-37285

* php
  * 307931-307934
  * 308262-308315
  * 308734-308761
  * 309111-309159
  * 309579-309580
  * 309688-309716
  * 309892-309910
  * 309986-310009
  * 310370-310389
  * 311346-311348

* gzip
  * 3eb6091d69a-884ef6d16c6
  * a1d3d4019ddd22-f17cbd13a1d0a7

* gmp
  * 13420-13421
  * 14166-14167

* libtiff
  * 0661f81-ac6a583
  * 0860361d-1ba75257
  * 3af26048-72391804
  * 4a24508-cc79c2b
  * 5b02179-3dfb33b
  * 829d8c4-036d7bb
  * 90d136e4-4c66680f
  * d13be72c-ccadf48a
  * d39db2b-4cd598c
  * ee2ce5b7-b5691a5a

* openssl
  * 1.0.1-beta1
