# 2026 土耳其旅行 — Google Maps 路線圖

用途：檢查每天移動是否順路、估算開車 / 步行疲勞。飛機段只列機場端點；自駕與步行段才用 directions 連結。

> **所有連結一律用座標，不用地名字串**（2026-08-20 全面改寫，來源：OSM Nominatim / Overpass 實查）。
> 原因是地名會被解成別的地方——原本的 `Grand Bazaar Istanbul` 指到**加拿大 South Surrey** 的同名店、`Harbour Street Ephesus` 指到**愛丁堡**，另有 12 個地名根本查不到。
> 例外只有四類仍用名稱：三個 IATA 機場加桃園 / 樟宜航廈（用名稱才會導到航廈而非跑道）、兩家熱氣球 / 駱駝業者（本來就是飯店接送）、以及 `Boris'in Yeri`（不在 OSM 上）。
> 連結顯示文字仍保留原本的地名，方便閱讀。

主文件索引：[進度.md](./進度.md) | [行程.md](./行程.md) | [餐廳安排.md](./餐廳安排.md) | [當日疲勞度.md](./當日疲勞度.md) | [Google-Maps路線圖.md](./Google-Maps路線圖.md) | [飯店預訂.md](./飯店預訂.md) | [租車預訂.md](./租車預訂.md) | [航班預訂.md](./航班預訂.md) | [待訂項目.md](./待訂項目.md) | [安安要做的事.md](./安安要做的事.md) | [豬豬要做的事.md](./豬豬要做的事.md)

## 已成形日期 Google Maps 路線圖

這段用來快速檢查「飯店是否順路」與每天移動方向。每日進度概覽中 `目前進度` 為 `已成形` 或 `已成形但有關鍵待訂` 的日期，都要在這裡有 Google Maps 路線圖。飛機段不適合用 Google Maps directions 判斷路線，所以只列機場端點；自駕與步行段才用 Google Maps 路線圖。打開連結後，Google Maps 有時會自動調整順序，出發前要再按當天實際時間檢查車程與營業狀態。

### 10/30（五）飛機上

| 路線 | Google Maps | 用途 |
|------|-------------|------|
| 安安出發端點：桃園機場 T2 | [地圖](https://www.google.com/maps/search/?api=1&query=Taiwan%20Taoyuan%20International%20Airport%20Terminal%202) | TK025 出發機場 |
| 豬豬出發端點：新加坡樟宜機場 T1 | [地圖](https://www.google.com/maps/search/?api=1&query=Singapore%20Changi%20Airport%20Terminal%201) | TK055 出發機場 |
| 抵達端點：Istanbul Airport | [地圖](https://www.google.com/maps/search/?api=1&query=Istanbul%20Airport) | 10/31 清晨集合與轉國內線 |

### 10/31（六）IST → ADB → Pikan Ephesus → 以弗所考古遺址 → Pikan Ephesus

| 段落 | Google Maps | 包含點位 | 判斷重點 |
|------|-------------|----------|----------|
| 飛機端點 | [IST](https://www.google.com/maps/search/?api=1&query=Istanbul%20Airport) / [ADB](https://www.google.com/maps/search/?api=1&query=Izmir%20Adnan%20Menderes%20Airport) | Istanbul Airport、Izmir Adnan Menderes Airport | 已訂 TK2320 11:00 IST → 12:10 ADB；這段靠航班，不用 Google Maps 車程判斷 |
| ADB 取車後自駕去飯店 | [ADB → Pikan Ephesus](https://www.google.com/maps/dir/?api=1&origin=Izmir%20Adnan%20Menderes%20Airport&destination=37.9489789,27.3671724&travelmode=driving) | ADB、Pikan Ephesus | 表定 **1h20**（實算 49 分 / 62.7 km）。**先進飯店 check-in 放行李**，14:40 抵達、入住 15:00 |
| 飯店 → 以弗所考古遺址 | [Pikan Ephesus → Ephesus Archaeological Site](https://www.google.com/maps/dir/?api=1&origin=37.9489789,27.3671724&destination=37.9355518,27.3461146&travelmode=driving) | Pikan Ephesus、以弗所考古遺址 | 表定 **10 分**（實算 5 分 / 3.7 km）。⚠️ **停在遺址入口旁的停車場**，比下入口好停 |
| 以弗所步行環線（回到停車處） | [遺址入口 → 大劇院 → 塞爾蘇斯圖書館 → 哈德良神廟 → 音樂廳 → 回遺址入口](https://www.google.com/maps/dir/?api=1&origin=37.9355518,27.3461146&destination=37.9355518,27.3461146&waypoints=37.9410660,27.3426916%7C37.9392052,27.3409200%7C37.9385230,27.3420025%7C37.9368337,27.3449823&travelmode=walking) | 遺址入口、大劇院 Great Theatre、塞爾蘇斯圖書館 Library of Celsus、哈德良神廟 Temple of Hadrian、音樂廳 Odeon | 15:10～17:40，走完回到停車處。串起這幾點的主街是克里特斯街 Curetes Street。冬季 18:00 關門，17:40 前往出口移動 |
| 以弗所 → 飯店 | [Ephesus Archaeological Site → Pikan Ephesus](https://www.google.com/maps/dir/?api=1&origin=37.9355518,27.3461146&destination=37.9489789,27.3671724&travelmode=driving) | 以弗所考古遺址、Pikan Ephesus | 表定 **10 分**（實算 5 分 / 3.5 km）。18:30 晚餐在飯店附近的 Selçuk 街上 |

### 11/01（日）Pikan Ephesus → Pamukkale → ADB → ASR → Henna

| 段落 | Google Maps | 包含點位 | 判斷重點 |
|------|-------------|----------|----------|
| 白天自駕與還車 | [Pikan Ephesus → 棉堡石灰棚 → Hierapolis → Theatre → Antique Pool → ADB](https://www.google.com/maps/dir/?api=1&origin=37.948976,27.367237&destination=Izmir%20Adnan%20Menderes%20Airport&waypoints=37.924483,29.119012%7C37.930954,29.126363%7C37.926772,29.129177%7C37.926095,29.125591&travelmode=driving) | Pikan Ephesus、棉堡石灰棚、Hierapolis、劇場、**Cleopatra Antique Pool 泡澡**、ADB | 單日約 430 公里的 V 字形折返。**08:30 出發**；Selçuk → 棉堡 2h20（實測 1h55）、棉堡 → ADB 2h40（實測 2h13）。**已排古董池泡澡，需帶泳衣**，泡池冬季 17:00 關門故排 14:00。**16:05 為離開棉堡的硬性上限**，表定 15:35 出發、18:15 抵達 ADB |
| 飛機端點 | [ADB](https://www.google.com/maps/search/?api=1&query=Izmir%20Adnan%20Menderes%20Airport) / [ASR Kayseri Airport](https://www.google.com/maps/search/?api=1&query=Kayseri%20Airport) | Izmir Adnan Menderes Airport、Kayseri Airport | 21:00 ADB → 22:35 ASR |
| ASR 深夜取車後自駕 | [Kayseri Airport → Henna Hotel - Adults Only](https://www.google.com/maps/dir/?api=1&origin=Kayseri%20Airport&destination=38.642261,34.828308&travelmode=driving) | ASR、Henna Hotel - Adults Only | 這段是深夜路線，重點是租車櫃台營業、航班延誤與駕駛疲勞 |

### 卡帕多奇亞三天的精確座標

11/02～11/04 的每一段都拆成**點到點單段連結**，不再用一條包 waypoints 的大弧線——因為 Google Maps 打開多點路線時會自作聰明重排順序，而這三天的順序是刻意設計的。下面每一列都只有一個 origin 和一個 destination，打開就是那一段。

| 點位 | 座標（OSM 實查 2026-08-19） | 用途 |
|------|------|------|
| Henna Hotel - Adults Only | `38.642261, 34.828308` | 11/01～11/03 住宿、熱氣球接送點、11/03 行李寄放點 |
| Göreme Open Air Museum | `38.6390591, 34.8455787` | 11/02 下午 |
| Kaymaklı 地下城 | `38.4599265, 34.7524882` | 11/03 第一站 |
| **鴿子谷觀景台** | `38.6320754, 34.8152333` | 11/03。⚠️ 導航要設**觀景台**，不要設「Güvercinlik Vadisi」谷地中心點（`38.6303780, 34.8130694`）——那個點在谷裡，導航會把你帶到產業道路 |
| Paşabağ 蘑菇谷 | `38.6770053, 34.8549063` | **11/02 上午（沒飛時）** |
| Zelve 露天博物館 | `38.6657426, 34.8652932` | **11/02 兩版都走**，離 Paşabağ 只有 1.8 km |
| Devrent 想像谷 | `38.6750753, 34.8843370` | 未排入，離 Zelve 4.4 km |
| Uçhisar Castle | `38.6304425, 34.8053230` | 11/03 |
| Çavuşin 老村 | `38.670828, 34.839455` | 11/03 下午。⚠️ 教堂因修復關閉，只走村子 |
| **愛情谷觀景台** | `38.663398, 34.829599` | 11/03 日落。OSM「Love Valley (Aşıklar Vadisi) Trail」，在 Göreme yolu 公路邊。⚠️ **不要用「Love Valley」谷地中心點**（`38.659038, 34.823152`）——那個在谷裡，導航會走產業道路（OSRM 把 2.6 km 算成 20 分） |
| **Henna Hotel - Adults Only** | `38.642261, 34.828308` | **11/01～11/04 連住三晚**，Göreme 鎮中心 Konak Sk. no:2/A |
| Sarı Han 商隊驛站 | `38.7118040, 34.9091913` | 11/04 |
| Kayseri Airport ASR | `38.7704, 35.4954` | 11/04 還車 |

### 11/02（一）Henna → 熱氣球 → 露天博物館 → 駱駝

> 全天四段自駕，共約 **50 分**，**兩版走的路線與順序完全相同**，只差出發時間與各點停留長度（有飛壓縮 40 分）。行李全天在房間內。晚餐 Topdeck Cave 走路 4 分鐘，**天黑後不用開車**。

**路線兩版共用**（沒飛 10:10 出發／有飛 12:00 出發）

| # | 段落（點到點） | 車程 | 判斷重點 |
|---|------|------|----------|
| A1 | [**Henna → Paşabağ 蘑菇谷**](https://www.google.com/maps/dir/?api=1&origin=38.642261,34.828308&destination=38.6770053,34.8549063&travelmode=driving) | **15 分**（實測 9.8 分 / 6.9 km） | 10:10 出發、10:25 到，逛到 11:15。最經典的多頭精靈煙囪，平地好走 |
| A2 | [**Paşabağ → Zelve 露天博物館**](https://www.google.com/maps/dir/?api=1&origin=38.6770053,34.8549063&destination=38.6657426,34.8652932&travelmode=driving) | **5 分**（實測 3.9 分 / **1.8 km**） | 11:15 出發、11:20 到，逛到 12:10。廢棄洞穴村，人比 Göreme 露天博物館少很多。✅ **官方是同一個景點「ZELVE-PAŞABAĞLAR」，票在 Paşabağ 買一次就通用**（€12），**每天開、08:00 開門** |
| A3 | [**Zelve → Göreme Open Air Museum**](https://www.google.com/maps/dir/?api=1&origin=38.6657426,34.8652932&destination=38.6390591,34.8455787&travelmode=driving) | **20 分** | 12:10 出發、12:30 進館，逛到 14:00 |
| A4 | [**Göreme Open Air Museum → Henna（鎮上午餐）**](https://www.google.com/maps/dir/?api=1&origin=38.6390591,34.8455787&destination=38.642261,34.828308&travelmode=driving) | **10 分** | 14:00 出發、14:10 到 | 回鎮上吃午餐，車停飯店；⚠️ 午餐尚未定店 |
| A2′ | **備援（幾乎不會用到）**：[Zelve → Devrent 想像谷](https://www.google.com/maps/dir/?api=1&origin=38.6657426,34.8652932&destination=38.6750753,34.8843370&travelmode=driving) | **6 分**（實測 5.8 分 / 4.4 km） | ✅ **Zelve 開放時間已官方查證（每天開、08:00 開門），原本的「怕沒開」風險已解除**，這條保留純粹當保險：真的遇到臨時封閉就往東開去 Devrent，逛 45 分，再走 [Devrent → Henna](https://www.google.com/maps/dir/?api=1&origin=38.6750753,34.8843370&destination=38.642261,34.828308&travelmode=driving)（**20 分**，實測 14.7 分 / 12 km），一樣 12:05 前回鎮上。**先寫好就不算現場決策** |
| — | Zelve 正常開的話**不加** Devrent | — | 行程夠滿了，加了會變成「要不要再跑一個」的現場決策 |

**接送段（不自駕）**

| # | 段落（點到點） | 車程 | 判斷重點 |
|---|------|------|----------|
| — | 熱氣球（接送，不自駕）：[Cappadocia Discovery Balloons](https://www.google.com/maps/search/?api=1&query=Cappadocia%20Discovery%20Balloons) | — | 已訂 11/02 06:00，Henna 接送。飛了 = 04:30～08:30；沒飛 = 這格空著，睡飽後 09:30 早餐。兩條線都在 **10:10 出發**走 A1～A5 |
| — | 駱駝（接送，不自駕，GetYourGuide `GYG996XFQRWK`）：[Cappadocia Camel Ride](https://www.google.com/maps/search/?api=1&query=Cappadocia%20Camel%20Ride) | — | **16:00 接送、騎乘約 16:20～17:20**，到 Henna 接。**11/02 日落 17:41**，整段騎乘都在黃金時段。含 Red / Rose（不含 Ortahisar），**自駕全程跳過**這幾點 |

**晚餐（步行，不自駕）**

| # | 段落（點到點） | 時間 | 判斷重點 |
|---|------|------|----------|
| W1 | [**Henna → Topdeck Cave Restaurant**](https://www.google.com/maps/dir/?api=1&origin=38.642261,34.828308&destination=38.6417558,34.8276558&travelmode=walking) | **步行 4 分**（約 0.3 km） | ✅ 已訂位 **18:30**、2 人 |
| W2 | [**Topdeck Cave → Henna**](https://www.google.com/maps/dir/?api=1&origin=38.6417558,34.8276558&destination=38.642261,34.828308&travelmode=walking) | **步行 4 分** | 20:15 走回，天黑後不用開車，兩人都能喝酒 |

**晚餐（步行，不自駕）**

| # | 段落（點到點） | 時間 | 判斷重點 |
|---|------|------|----------|
| W1 | [**Henna → Seten Restaurant**](https://www.google.com/maps/dir/?api=1&origin=38.642261,34.828308&destination=38.6412661,34.8257096&travelmode=walking) | **步行 8 分**（約 630 m） | 11/03 晚餐：**沒飛 18:15 / 補飛 17:35**（補飛趕得上日落前）。⚠️ 不接受訂位，客滿就鎮上另找 |
| W2 | [**Seten → Henna**](https://www.google.com/maps/dir/?api=1&origin=38.6412661,34.8257096&destination=38.642261,34.828308&travelmode=walking) | **步行 8 分** | 走回去，天黑後不用開車 |

### 11/03（二）Henna → Kaymaklı → 鴿子谷 → Uçhisar → Çavuşin → 愛情谷 → 回 Henna

> 路線是「**南下 → 北返 → 北上看日落**」：Göreme（中）→ **Kaymaklı（南，第一站）** → 鴿子谷 / Uçhisar（西，Göreme 後院）→ **Çavuşin（北）** → **愛情谷觀景台（北，日落）** → 回 Göreme。
>
> **連住 Henna 三晚，這天不用退房、不用寄放行李、不用折返。** 行李整天在房間，車上只放小包、水、零食。
>
> 車程總計 **100 分**（35 + 40 + 5 + 15 + 5 + 5）。

| # | 段落（點到點） | 車程 | 時間 | 判斷重點 |
|---|------|------|------|----------|
| 1 | [**Henna → Kaymaklı 地下城**](https://www.google.com/maps/dir/?api=1&origin=38.642261,34.828308&destination=38.4599265,34.7524882&travelmode=driving) | **35 分** | 09:30～10:05 | 32 km，全天最長的一段，放在最有精神的時候。⚠️ **唯一還沒用 Google 直接量過的路段**（OSRM 推估 27～29 分），出發前補查一次。✅ Kaymaklı 開放時間已官方查證：**每天開、08:00 開門**（09:35 進場沒問題） |
| 2 | [**Kaymaklı 地下城 → 鴿子谷觀景台**](https://www.google.com/maps/dir/?api=1&origin=38.4599265,34.7524882&destination=38.6320754,34.8152333&travelmode=driving) | **40 分** | 11:35～12:15 | 約 18 km，走 Uçhisar–Nevşehir 路，**不經 Göreme**。反向已實測 28 分。鴿子谷只停 **30 分** |
| 3 | [**鴿子谷觀景台 → Uçhisar Castle**](https://www.google.com/maps/dir/?api=1&origin=38.6320754,34.8152333&destination=38.6304425,34.8053230&travelmode=driving) | **5 分** | 12:45～12:50 | 相鄰，3.9 km。中間插 Uçhisar 午餐 12:50～13:50，Castle 13:55～14:55 |
| 4 | [**Uçhisar Castle → Çavuşin 老村**](https://www.google.com/maps/dir/?api=1&origin=38.6304425,34.8053230&destination=38.670828,34.839455&travelmode=driving) | **15 分** | 15:05～15:20 | 7.4 km（OSRM 11 分）。⚠️ **Çavuşin 教堂因修復關閉**（muze.gov.tr `SectionId=CAV01` 標示 KAPALI），只走村子與崖下 |
| 5 | [**Çavuşin → 愛情谷觀景台**](https://www.google.com/maps/dir/?api=1&origin=38.670828,34.839455&destination=38.663398,34.829599&travelmode=driving) | **5 分** | 16:20～16:25 | ✅ 已實測，1.6 km、OSRM 2.2 分、均速 43 km/h。觀景台座標 `38.663398, 34.829599` 取自 OSM「Love Valley (Aşıklar Vadisi) Trail」，在 **Göreme yolu 公路邊** |
| 6 | [**愛情谷觀景台 → Henna**](https://www.google.com/maps/dir/?api=1&origin=38.663398,34.829599&destination=38.642261,34.828308&travelmode=driving) | **5 分** | 17:50～17:55 | ✅ 已實測，3.0 km、OSRM 3.8 分。日落 17:40，天剛黑就到家 |

**今天飛（熱氣球在 11/03）：路線整個倒過來走**，因為 **Kaymaklı 冬季 08:00–17:00、末班入場約 16:00**，照上面的順序把它放最後會 15:45 才到。倒著走之後補眠從 1 小時變 3 小時，鴿子谷也換到日落金色時段：

| # | 段落（點到點） | 車程 | 時間 |
|---|------|------|------|
| F1 | [**Henna → Uçhisar Castle**](https://www.google.com/maps/dir/?api=1&origin=38.642261,34.828308&destination=38.6304425,34.8053230&travelmode=driving) | **7 分** | 11:40～11:47 |
| F2 | [**Uçhisar Castle → Seki**](https://www.google.com/maps/dir/?api=1&origin=38.6304425,34.8053230&destination=38.6300930,34.8075940&travelmode=walking)（步行） | **2 分** | 12:55～12:57，13:00 入座 |
| F3 | [**Uçhisar → Kaymaklı**](https://www.google.com/maps/dir/?api=1&origin=38.6304425,34.8053230&destination=38.4599265,34.7524882&travelmode=driving) | **30 分** | 14:00～14:30 |
| F4 | [**Kaymaklı → 鴿子谷觀景台**](https://www.google.com/maps/dir/?api=1&origin=38.4599265,34.7524882&destination=38.6320754,34.8152333&travelmode=driving) | **40 分** | 16:00～16:40，停 **30 分** |
| F5 | [**鴿子谷 → Henna**](https://www.google.com/maps/dir/?api=1&origin=38.6320754,34.8152333&destination=38.642261,34.828308&travelmode=driving) | **10 分** | 17:10～17:20 |

補飛版車程 **87 分**，Uçhisar → Kaymaklı 只要 30 分 / 28.8 km，比從 Göreme 出發的 35 分還短。

**縮短版（太累時）**：砍 **Uçhisar Castle**（省 65 分，14:00 就回得到飯店）——第 3 段直接接 [鴿子谷觀景台 → Henna](https://www.google.com/maps/dir/?api=1&origin=38.6320754,34.8152333&destination=38.642261,34.828308&travelmode=driving)。

**地下城選 Kaymaklı 不選 Derinkuyu**：Derinkuyu 更深更震撼，但要再往南多開 10 公里。

### 11/04（三）Henna → Avanos → Sarı Han 商隊驛站 → ASR → Istanbul

> 目前狀態：已成形。當天最後一個點是 **Sarı Han 商隊驛站**（1249 年塞爾柱商隊旅館，離 Avanos 約 6～8 km、往 ASR 方向），補上全程唯一缺席的塞爾柱時期建築。不安排陶藝購買，因為當天要接一段托運僅 15kg 的國內線。航班 TK2017 ASR → IST 已開票。
>
> 車程已實查（OSRM，並以已由 Google Maps 實測的 Avanos→ASR 校準）。Sarı Han 座標 38.7118, 34.90919，在 Avanos 正東 5.8 km、往 ASR 方向。開放 **每天 09:00–18:00**，無另列冬季時間。

> ⚠️ **這是唯一行李必須待在車上的一天**（10:00 退房後無處可放，Mustafapaşa + Avanos + Sarı Han 三個停點共約 3 小時）。取車當天的後車廂防護清單見 [租車預訂.md](./租車預訂.md)。

**主線（四個 Plan 共用）— 點到點**

| # | 段落（點到點） | 車程 | 時間 | 判斷重點 |
|---|------|------|------|----------|
| 1 | [**Henna → Avanos**](https://www.google.com/maps/dir/?api=1&origin=38.642261,34.828308&destination=38.718737,34.846866&travelmode=driving) | **12 分**（OSRM 11 分 ×1.08） | 12:00 出發、12:15 到 | 9.5 km。改住 Göreme 鎮中心後，這段從 45 分縮成 12 分 |
| 2 | [**Avanos → Sarı Han 商隊驛站**](https://www.google.com/maps/dir/?api=1&origin=38.718737,34.846866&destination=38.7118040,34.9091913&travelmode=driving) | **10 分**（實查 7 分） | 14:25～14:35 | 7.0 km，在 Avanos 正東、往 ASR 方向，**不是繞路**。Avanos 13:15～14:25 河邊午餐，**不買陶器** |
| 3 | [**Sarı Han → Kayseri Airport ASR**](https://www.google.com/maps/dir/?api=1&origin=38.7118040,34.9091913&destination=Kayseri%20Airport&travelmode=driving) | **1h05**（實查 53 分） | 15:20～16:25 | 60.5 km，中途加油。Sarı Han 14:35～15:20（09:00–18:00 開放）；**15:35 為離開 Sarı Han 的硬性上限**；16:25～16:45 還車 |

**今天飛：熱氣球補飛在 11/04**

| # | 段落 | 車程 | 判斷重點 |
|---|------|------|----------|
| — | 熱氣球（接送，不自駕）：**Henna 接** | — | Göreme 鎮中心是標準接送範圍，**不用特別安排**；04:40 接、06:00～07:30 飛、09:00 送回。仍建議前一天跟司機確認會合點 |
| 1' | 早餐 08:30～10:00 → **10:00 退房** | — | 熱氣球 08:30 就結束，白天完全接回主線 |
| 1'' | 累的話**不必跳過 Avanos**，只要縮成 1h15（12:15～13:30）| — | 從 Göreme 出發只要 12 分，13:40 就能進 Sarı Han，15:45 到 ASR，比主線早 30 分 |

**雨天 / 時間吃緊備案**

| 段落 | Google Maps | 判斷重點 |
|------|-------------|----------|
| 跳過 Avanos 與 Sarı Han | [Henna → Mustafapaşa → Ürgüp → Kayseri Airport](https://www.google.com/maps/dir/?api=1&origin=38.642261,34.828308&destination=Kayseri%20Airport&waypoints=38.583396,34.896916%7C38.630051,34.911603&travelmode=driving) | Mustafapaşa 30 分短停 + Ürgüp 午餐 → ASR |

**其餘段落**

| 段落 | Google Maps | 包含點位 | 判斷重點 |
|------|-------------|----------|----------|
| 飛機端點 | [ASR Kayseri Airport](https://www.google.com/maps/search/?api=1&query=Kayseri%20Airport) / [Istanbul Airport IST](https://www.google.com/maps/search/?api=1&query=Istanbul%20Airport) | ASR、IST | 已訂 TK2017 18:40 ASR → 20:20 IST；目標 16:30 完成還車 / 抵達航廈。⚠️ Rentalcars 訂單上的還車時間是 **19:00**，晚於起飛時間，需與 AVEC / Rentalcars 確認可提早還車 |
| IST → Basilissis Hotel | [Istanbul Airport → Basilissis Hotel](https://www.google.com/maps/dir/?api=1&origin=Istanbul%20Airport&destination=41.010415,28.978109&travelmode=driving) | IST、Basilissis Hotel | Klook 接機已訂：11/04 20:20，IST → Basilissis Hotel，經濟車型 4 人座（最多 3 人 / 2 件行李），2 位乘客，已綁定 TK2017、含舉牌服務、免費等候 60 分鐘，實付 NT$1,630，免費取消至 11/03 20:20；領完行李到接機大廳找舉牌司機 |

### 11/05（四）Basilissis Hotel → Karakoy / Galata / Eminonu → Basilissis Hotel

| 段落 | Google Maps | 包含點位 | 判斷重點 |
|------|-------------|----------|----------|
| 新城暖身主線 | [Basilissis Hotel → Boris'in Yeri → Galata Tower → Sokak Lezzeti Tarihi Balık Dürümcü Mehmet Usta → Galata Bridge → Eminonu](https://www.google.com/maps/dir/?api=1&origin=41.010415,28.978109&destination=41.017996,28.974141&waypoints=Boris%27in%20Yeri,%20Fatih,%20%C4%B0stanbul%7C41.025640,28.974213%7C41.024425,28.978617%7C41.020076,28.973087&travelmode=transit) | Basilissis、Boris'in Yeri、Galata、Karakoy Balık Dürüm、Galata Bridge、Eminonu | 11/05 早餐固定在 Boris'in Yeri；Balık Dürüm 放 Karakoy 當輕午餐 / 點心，早餐吃太飽就兩人分一份 |
| 香料市集 / Suat Usta 晚餐回程 | [Spice Bazaar → Suat Usta Mersin Tantuni Taksim → Basilissis Hotel](https://www.google.com/maps/dir/?api=1&origin=41.016463,28.971098&destination=41.010415,28.978109&waypoints=41.034666,28.982851&travelmode=transit) | Spice Bazaar、Taksim Suat Usta、Basilissis | Suat Usta 適合 11/05 晚上接新城區；若當天吃太飽，延到 11/07 晚上替代 Olden 1772 |

### 11/06（五）Basilissis Hotel → Sultanahmet 舊城核心 → Basilissis Hotel

| 段落 | Google Maps | 包含點位 | 判斷重點 |
|------|-------------|----------|----------|
| 舊城步行主線 | [Basilissis Hotel → Basilica Cistern → Hagia Sophia → Blue Mosque → Seven Hills Restaurant → Grand Bazaar → Hafız Mustafa 1864 Sirkeci → Basilissis Hotel](https://www.google.com/maps/dir/?api=1&origin=41.010415,28.978109&destination=41.010415,28.978109&waypoints=41.008479,28.978382%7C41.008504,28.980011%7C41.005384,28.976853%7C41.006371,28.979714%7C41.010967,28.968253%7C41.016010,28.973360&travelmode=walking) | Basilissis、地下水宮殿、聖索菲亞、藍色清真寺、Seven Hills、Grand Bazaar、Hafiz Mustafa | 這是 Basilissis 的最大優勢，早上可步行進舊城核心避人潮；14:15～16:15 固定 Grand Bazaar；托卡匹皇宮已拿掉 |

### 11/07（六）Basilissis Hotel → Hammam → Vefa Bozacisi → Kadikoy / Uskudar 或 Karakoy → Basilissis Hotel

| 段落 | Google Maps | 包含點位 | 判斷重點 |
|------|-------------|----------|----------|
| 土耳其浴 + Vefa Bozacisi | [Basilissis Hotel → Turkish Bath Hammam → Vefa Bozacisi → Basilissis Hotel](https://www.google.com/maps/dir/?api=1&origin=41.010415,28.978109&destination=41.010415,28.978109&waypoints=41.012140,28.958548%7C41.015318,28.958420&travelmode=walking) | Basilissis、hammam、Vefa Bozacisi | 浴後順路 [Vefa Bozacisi](https://maps.app.goo.gl/scQBEiTX13GjXswQA)；浴場選 Sultanahmet / Sirkeci 一帶，與 Vefa 同區；20～30 分喝杯 boza 即可 |
| 亞洲側生活線 | [Basilissis Hotel → Eminonu → Kadikoy → Uskudar → Basilissis Hotel](https://www.google.com/maps/dir/?api=1&origin=41.010415,28.978109&destination=41.010415,28.978109&waypoints=41.017996,28.974141%7C40.991295,29.024563%7C41.026549,29.015132&travelmode=transit) | Basilissis、Eminonu、Kadikoy、Uskudar | 若天氣好且體力夠，從 Eminonu / Karakoy 搭渡輪去 Kadikoy；Uskudar 作夕陽 / 海峽視角加分項，不硬排 |
| 低移動替代線 | [Basilissis Hotel → Karakoy → Galata → Basilissis Hotel](https://www.google.com/maps/dir/?api=1&origin=41.010415,28.978109&destination=41.010415,28.978109&waypoints=41.022864,28.974039%7C41.025640,28.974213&travelmode=transit) | Basilissis、Karakoy、Galata | 若土耳其浴後很放鬆或天氣差，就不要跨亞洲側；用 T1 / 叫車到 Karakoy / Galata 吃飯散步即可 |
| 超市後晚餐線 | [Basilissis Hotel → Olden 1772 → Basilissis Hotel](https://www.google.com/maps/dir/?api=1&origin=41.010415,28.978109&destination=41.010415,28.978109&waypoints=41.014927,28.974103&travelmode=walking) | Basilissis、Olden 1772 | 11/07 傍晚超市買完先回飯店放東西，再步行 / 短程叫車去 Olden 1772；若想更輕鬆，改飯店附近晚餐 |

### 11/08（日）Basilissis Hotel → Istanbul Airport 回程

| 段落 | Google Maps | 包含點位 | 判斷重點 |
|------|-------------|----------|----------|
| 早餐 + 採買收尾線 | [Basilissis Hotel → 早餐主選 → Şok Sirkeci → Basilissis Hotel](https://www.google.com/maps/dir/?api=1&origin=41.010415,28.978109&destination=41.010415,28.978109&waypoints=41.003864,28.978764%7C41.013436,28.975343&travelmode=walking) | Basilissis、早餐主選、Şok Sirkeci | **托卡匹皇宮已拿掉**。飯店 → 早餐 12 分、早餐 → Şok 20 分、Şok → 飯店 9 分；Şok **週日 09:00–21:00** |
| Basilissis Hotel → IST | [Basilissis Hotel → Istanbul Airport](https://www.google.com/maps/dir/?api=1&origin=41.010415,28.978109&destination=Istanbul%20Airport&travelmode=driving) | Basilissis Hotel、IST | Trip.com 送機已訂（⚠️ 與接機不同平台）：11/08 13:00，Basilissis Hotel → IST，訂單 1616334355549226、車行追蹤碼 88B5DYZ（UNITED INNOVATION），已綁定 TK124，預估 51 km / 52 分，先乘後付 TWD 1,309，免費取消至 11/08 07:00；⚠️ 免費等候僅 15 分鐘；不退稅，目標 14:30 前抵達 IST |
| 回程機場端點 | [Istanbul Airport IST](https://www.google.com/maps/search/?api=1&query=Istanbul%20Airport) | IST | 11/08 建議 14:30 前抵達 IST；安安 17:15 起飛，豬豬 18:30 起飛 |


## Google Maps 使用建議

1. 在 Google Maps 建一個清單，例如：`2026 Turkey`
2. 先收藏機場、住宿、每天想去的景點與交通點
3. 用標籤區分：
   - `必去`
   - `想去`
   - `咖啡`
   - `雨天備案`
   - `行李寄放`
4. 每天出門前只看當天同區域的點，避免行程太散

如果想做更完整的地圖路線，可以再建立 [Google My Maps](https://www.google.com/maps/d/)，把每天用不同顏色分層。

### 伊斯坦堡新增點位（2026-09-30）

| 點位 | 座標 | 備註 |
|------|------|------|

| 多爾瑪巴切皇宮 | `41.038961, 28.999773` | 11/06。09:00–17:30，週一休，售票口 17:00 關 |
| 奧塔科伊 Büyük Mecidiye Camii | `41.047287, 29.026772` | 11/06 午餐 kumpir |
| Kabataş | `41.033870, 28.994202` | T1 終點、F1 纜車下站、渡輪碼頭 |
| 塔克辛廣場 | `41.037833, 28.985017` | 獨立大街北端 |
| Tünel（F2 下站） | `41.025850, 28.974059` | 獨立大街南端，加拉達塔旁 |
| **BUSFORUS Sultanahmet Meydanı 站** | `41.007723, 28.977940` | 11/05 **地下水宮殿導覽團集合點**。⚠️ **不是地下水宮殿入口**——在聖索菲亞對面（At Meydanı Cd. No:3），認紅色雙層觀光巴士站與導遊的白橘色 Istanbul E-pass 旗。聖索菲亞走過來 311 m / 4 分；集合點到地下水宮殿入口 108 m / 1 分 |
| **Kabataş İskelesi** | `41.032935, 28.994153` | 11/07 日落遊船**上船點**。T1 終點站走 162 m |
| **Karaköy İskelesi** | `41.021429, 28.976732` | 11/07 日落遊船**下船點**。到 Olden 1772：過加拉達橋 988 m / 13 分，或 T1 一站 |
| Turyol 碼頭 | `41.018738, 28.970381` | 通票沒買時的遊船備案。⚠️ 在**加拉達橋西側**，不是東側的市政渡輪碼頭 |
