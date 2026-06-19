# didi-travel-world

旅遊計劃網站，以靜態 HTML 頁面呈現每趟旅行的每日行程。

## 專案結構

```
didi-travel-world/
├── index.html          # 旅行總覽首頁（深色風格，卡片列表）
├── huadong/
│   └── index.html      # 花東四日行程（2026/07/15–18）
└── turkey/
    ├── index.html      # 土耳其11日行程（2026/10月）
    └── DIDI_integration_202610伊斯坦堡_旅行計劃.md
```

## 技術規範

- 每個旅行計劃為**單一 HTML 檔案**，無外部 JS 依賴（Google Fonts 除外）
- **Mobile-first**，以 iPhone Safari 為主要測試目標
- 互動式每日投影片，支援左右滑動手勢切換
- 每個子頁面**必須包含返回 `../index.html` 的按鈕**

## 新增旅遊計劃 SOP

1. 在根目錄新增 `<trip-name>/index.html`
2. 使用 `frontend-design` skill 建立頁面，設計風格對應目的地文化
3. 頁面頂端加入返回總覽的按鈕（參考 huadong/index.html 的 `.back-btn` 實作）
4. 在根目錄 `index.html` 的 `.trips-grid` 新增對應 `.trip-card`

## 設計慣例

- 每趟旅行有獨立的**色彩主題**（CSS variables）
- 每日投影片以 `data-day` attribute 區分，搭配 `[data-day="N"]` CSS selector 套用主題色
- 時間軸 `.tl` 左側 gutter 需足夠寬，避免 `.tl-time` 與 `.tl-dot` 重疊（padding-left ≥ 72px）
- 住宿資訊以 `.stay-chip` 呈現於每日最下方

## GitHub

- Repo: `https://github.com/RicChu/didi-travel-world`
- Branch: `main`
- 修改後 commit + push 到 GitHub Pages
