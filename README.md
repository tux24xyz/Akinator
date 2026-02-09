# Akinator

一個完全 Vibe-coding 出來的 AI 神燈精靈遊戲，玩家在心中想任何一個二次元角色，語言模型會問二十題是非題來猜。

## 使用方法

`git clone` 整個專案下來後，在主資料夾新增一個 `.env` 檔，填入以下內容：

```
GEMINI_API_KEY=你的_API_KEY_貼在這裡
FLASK_SECRET=這是一串隨機字串用來加密Session # 亂寫就好
```

貼上 Google AI Studio 的 API Key 就可以用了，預設模型是 `gemini-2.5-flash`。

## System prompt

目前語言模型的角色設定是逆轉裁判系列的男主角：成步堂龍一。可以自己修改改
