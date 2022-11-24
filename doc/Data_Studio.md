# Data Studio
## Phase I
### 設計專用、標準、可擴展的 Data API 服務架構 
( 2021/12/31 release 2022/02/21 updated)
#### 專用
既有對外提供服務的 Data API 多為在既有的報表服務上進行延伸，往往在提供資料服務時，影響既有報表服務效能。
因此，Data Studio 的首要目標，即在將服務分流至 Data Studio 的 Data Service Platform，提供專用服務。此專用服務除了分流外，亦加入或提升在流量管控、安全性以及使用者稽核等功能。
#### 標準
不同報表系統之間，由於系統負責人或開發人員不同，撰寫 Data API 的方法不盡相同。除了造成使用者使用上的不便外，亦造成跨系統需進行分享或整合時的困難。
在 Data Studio 以三個層次進行標準化： 
- 資料服務端點標準化：
TTL(Transparent Transition Layer) 通透轉換層，以來源轉換器 (Source Adapter) 接軌各種類型的 Data API 以及異質資料庫，轉成以 RESTful API 的形式，定義每一個具名資料的服務端點並以之提供對外服務。
- 具名資料標準化：
[Named Data Entity](https://hackmd.io/6e37jj7pSdyJ9G9k__633Q) 以[RDF]()、[RDFS]()、[URI]() 表示，並且可以對到一個具名資料的服務端點。
- 語意表示標準化：
[FOL](), [Ontology](), [Semantic Web]()
#### 可擴展
可分為服務領域擴展以及服務容量擴展
- 服務領域擴展
    - 以業務領域定義服務藍圖 (Business Domain --> Service Blueprint )，如在前段工廠即區分 mfg, int, eng 等至少三個業務領域，每一個業務領域可以獨立建制領域內的服務端點。依此架構，其他業務領域只要遵照開發規範，即可以[聯邦式的結構]()加入服務。
- 服務容量擴展
    - 藉由如 nginx 的負載平衡器，可進行 api 請求的負載平衡外，在必要時增加資料服務器的數量，以因應服務容量的不足。
    - 依照業務領域建置之領域內服務端點集合[set of sevice end points for a business domain]，與主要服務端點[ds api portal]為鬆耦合型態，可付著於主要服務端點，亦可在必要時獨立於主要端點之外，使用獨立的服務架構。

### 樣品屋實作
以以上所設計之服務架構，擇數個 user 所需之資料服務進行樣品屋的實作。（預計 2022/02/28 完成 mfg/<fab>/<product>/<route V recipe V qtime>
eng/<fab>/<equipment>/<sub_equipment>/edc_raw )

## Phase II
### Data Studio Portal
 A data studio portal host the navigator, swagger api and NDE query etc.
### Build EDW use cases
#### Source Adapter on EDW
 
### Build Data Lake use cases
#### Adapter on Data Lake

## Phase III
### Enhancement of Service Architecture
- Caching Mechanism
- Queuning 
- Abnormally detection
### Roll-out another business domain
