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

## 旅行狀態分類規則

`index.html` 的卡片分為兩個 section：
- **即將出發**（`.section-label.upcoming`）：出發日期尚未到達
- **已完成**（`.section-label.completed`）：回程日期已過，卡片加上 `.done` class（灰階淡化效果）

**每次任何修改執行完畢前，必須比對今天日期與各旅行的回程日期**：
- 若旅行回程日已過 → 確認後將卡片從「即將出發」移至「已完成」並加 `.done` class
- 若日期不確定 → 詢問使用者

目前各旅行日期：
| 旅行 | 出發 | 回程 | 狀態 |
|------|------|------|------|
| 花東縱谷 | 2026-07-15 | 2026-07-18 | 計劃中 |
| 土耳其之旅 | 2026-10-xx | 2026-10-xx | 計劃中 |

## 新增旅遊計劃 SOP

1. 在根目錄新增 `<trip-name>/index.html`
2. 使用 `frontend-design` skill 建立頁面，設計風格對應目的地文化
3. 頁面使用 `.app-topbar > .back-btn` 結構（嵌入 flex 流，非 fixed）返回 `../index.html`
4. 在根目錄 `index.html` 的「即將出發」`.trips-grid` 新增對應 `.trip-card`
5. 更新 CLAUDE.md 旅行狀態表

## 設計慣例

- 每趟旅行有獨立的**色彩主題**（CSS variables）
- 每日投影片以 `data-day` attribute 區分，搭配 `[data-day="N"]` CSS selector 套用主題色
- 時間軸三欄佈局：`[time 60px] [4px gap] [line/dot] [4px gap] [card]`，`.tl` padding-left:77px；`.tl-time` width:60px left:-77px；`.tl-dot` left:-13px；`.tl::before` left:64px。這樣可容納 `11:30–12:30` 等較長時間文字，且三欄完全不重疊。
- 子頁面返回按鈕使用 `.app-topbar > .back-btn` 結構，嵌入 `.app` flex 流（非 `position:fixed`），避免覆蓋內容
- 住宿資訊以 `.stay-chip` 呈現於每日最下方

## GitHub

- Repo: `https://github.com/RicChu/didi-travel-world`
- Branch: `main`
- 修改後 commit + push 到 GitHub Pages
