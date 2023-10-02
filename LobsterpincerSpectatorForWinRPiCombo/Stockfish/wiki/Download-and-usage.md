# Download Stockfish

_Note: Stockfish is a **command line program**. You may want to use it in your own UCI-compatible [chess GUI](#download-a-chess-gui)._

## Get started

1. First download Stockfish. There are multiple choices. Refer to the [official](#official-downloads) and [unofficial](#unofficial) downloads. Stockfish itself is *completely free* with all its options.
2. Next, [download a GUI](#download-a-chess-gui) (Graphical User Interface) as it is needed to conveniently use Stockfish. There are multiple free and commercial GUIs available. Different GUI's have more or less advanced features, for example, an opening explorer or automatic game analysis.
3. Now Stockfish must be made available to the GUI. [Install in a Chess GUI](#install-in-a-chess-gui) explains how this can be done for some of them. If a different GUI is used, please read the GUI's manual.
4. Ultimately, change the default [settings](#change-settings) of Stockfish to get the [best possible analysis](Stockfish-FAQ#optimal-settings).

---
## Official downloads

### Latest release

https://stockfishchess.org/download/

* [Windows](https://stockfishchess.org/download/windows/)
* [Linux](https://stockfishchess.org/download/linux/)
* macOS
  * [App Store](https://itunes.apple.com/us/app/stockfish/id801463932?ls=1&mt=12)
  * `brew install stockfish`
* [iOS](https://itunes.apple.com/us/app/smallfish-chess-for-iphone/id675049147?mt=8)

### Latest development build

1. Navigate to our [releases](https://github.com/official-stockfish/Stockfish/releases?q=prerelease%3Atrue)
2. Expand the Assets
3. Download your preferred binary

## Choose a binary

In order of preference:
1. BMI2
   * Intel: 4th Gen and newer (e.g. i7 4770K, i5 13600K).
   * AMD: Zen 3 and newer (e.g. Ryzen 5 5600X, Ryzen 9 7950X).
2. AVX2
   * AMD: Zen, Zen+ and Zen 2 (e.g. Ryzen 5 1600, Ryzen 5 3600).
3. Modern
4. 64-bit
5. 32-bit

---

# Download a Chess GUI

A chess graphical user interface allows you to interact with the engine in a user-friendly way. Popular GUIs are:

## Free

* [Arena](http://www.playwitharena.de/)
  * [How to install Stockfish](#arena)
  * [Change settings](#arena-1)
* [Nibbler](https://github.com/rooklift/nibbler/releases/latest) ([source code](https://github.com/rooklift/nibbler))
  * [How to install Stockfish](#nibbler)
  * [Change settings](#nibbler-1)
* [Lichess Local Engine](https://github.com/fitztrev/lichess-tauri/releases/latest) ([source code](https://github.com/fitztrev/lichess-tauri)) (**WIP**)
  * [How to install Stockfish](#lichess-local-engine)
  * [Change settings](#lichess)
* [BanksiaGUI](https://banksiagui.com/download/)
* [Cutechess](https://github.com/cutechess/cutechess/releases/latest) ([source code](https://github.com/cutechess/cutechess))
* [ChessX](https://chessx.sourceforge.io) ([source code](https://sourceforge.net/projects/chessx/))
* [Lucas Chess](https://lucaschess.pythonanywhere.com/downloads) ([source code](https://github.com/lukasmonk/lucaschessR2))
* [Scid vs. PC](https://scidvspc.sourceforge.net/#toc3) ([source code](https://sourceforge.net/projects/scidvspc/))
* [XBoard](https://www.gnu.org/software/xboard/#download) ([source code](https://ftp.gnu.org/gnu/xboard/))

## Paid

* [Chessbase](https://chessbase.com/)
* [Hiarcs](https://www.hiarcs.com/chess-explorer.html)
* [Shredder](https://www.shredderchess.com/)

## Online

_Note: If you don't want to download a GUI, you can also use some of the available online interfaces. Keep in mind that you might not get the latest version of Stockfish, settings might be limited and speed will be slower._

* [Lichess](https://lichess.org/analysis)
  * [Change settings](#lichess)
* [Chess.com](https://www.chess.com/analysis)
  * [Change settings](#chesscom)

---

# Install in a Chess GUI

## Arena

1. Engines > Install New Engine...

    <img src="https://user-images.githubusercontent.com/63931154/206901675-33341f5f-03c7-4ca1-aaa5-185a2a7f5b83.png" width="300">

2. Select and open the Stockfish executable

    <img src="https://user-images.githubusercontent.com/63931154/206901703-a6538e9f-352b-4a6e-9c89-be804d57f010.png" width="300">

## Nibbler

1. Engine > Choose engine...

    <img src="https://user-images.githubusercontent.com/63931154/206902163-8a92d15c-0793-4b1a-9f9c-c5d8a9dd294e.png" width="300">

2. Select and open the Stockfish executable

    <img src="https://user-images.githubusercontent.com/63931154/206902197-0062badd-3d12-45dd-b19f-918edfbb22ca.png" width="300">

## Lichess Local Engine

1. Log in with Lichess

    <img src="https://user-images.githubusercontent.com/63931154/232722746-b85d345f-e455-4d62-ad33-98d29756d51c.png" width="300">

    <img src="https://user-images.githubusercontent.com/63931154/232723150-5e51029a-b345-4789-b12d-beef91c7e835.png" width="300">

2. Click the Install Stockfish button

    <img src="https://user-images.githubusercontent.com/63931154/232723405-8c15861d-578d-432b-a009-362d63bd69d0.png" width="300">

3. Go to the Lichess analysis page

   https://lichess.org/analysis

4. Select the engine in the engine manager

    <img src="https://user-images.githubusercontent.com/63931154/232724185-b3427cd5-8a7e-4dca-aa76-7e3afdd81c0f.png" width="300">

---

# Change settings

_Note: Please check our [FAQ guide](Stockfish-FAQ#optimal-settings) to set the optimal settings._

## Arena

* Right click in the engine name > Configure

    <img src="https://user-images.githubusercontent.com/63931154/206901924-aad83991-dfde-4083-a29c-a565effca034.png" width="300"><br>
    <img src="https://user-images.githubusercontent.com/63931154/206913983-82b8cf42-2a03-4896-9511-3472b1185a7e.png" width="300">

## Nibbler

* In the Engine section

    <img src="https://user-images.githubusercontent.com/63931154/206902419-4a2a5580-2d66-4ea1-97f2-93bc2ff846bd.png" width="300">

## Lichess

* In the menu

    <img src="https://user-images.githubusercontent.com/63931154/206903008-a672ea93-09a0-4ca7-94e0-2d1228c7c25d.png" width="300">

## Chess.com

* In the settings

    <img src="https://user-images.githubusercontent.com/63931154/206903150-e0fa28c8-60dd-4f82-aea2-5cf35c6fa56d.png" width="300"><br>
    <img src="https://user-images.githubusercontent.com/63931154/206903463-d96e3a59-52b6-4966-aed2-716c9f9c6c24.png" width="300">
