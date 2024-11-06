# WhiskyRCM

프로젝트에 대한 자세한 사항은 아래 노션에 정리되어있다.   
   
![js](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white)  
https://shrub-bone-411.notion.site/1a147c08fbb449688e67304df21733f6?pvs=4
   
![js](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![js](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![js](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)  
   
***
   
이 프로젝트는 순전히 개인적인 고민에서 시작되었다. 위스키를 고를 때 바에서 주문할 때처럼 바텐더에게 추천을 받으면 되지만 그 바텐더가 언제나 내 옆에 있는 것은 아니다. 마트나 면세점에서 바틀을 구매할 때 혹은 바에서 주문을 할 때 바텐더에게 추천을 받지 않고 '난 원래 이 위스키에 대해 알고 있어~'하는 가오를 잡고 싶을 때는 그 술에 대해 알고 있어야 할 것이다. 이 프로젝트는 이러한 고민을 줄여준다. 사용자가 자신의 취향을 입력하면 그에 맞는 위스키를 추천해준다. 대략적인 가격과 간략한 설명도 함께 알려준다. 이 프로젝트가 취향에 맞는 위스키를 고르는 데에 작게나마 도움이 되었으면 좋겠다.   
위스키에 대한 데이터는 https://whiskyadvocate.com 을 참고했다.   
이 프로젝트는 VectorDB를 사용하는 데에 의의를 둔다. 위스키에 대한 정보가 텍스트로 이루어져 있기 때문에 데이터 저장은 물론이고 쿼리를 날리면 그에 따른 유사도 거리를 측정하여 가장 근접한 결과를 보여주는 것까지 DB에서 한번에 가능하다는 것이 아주 놀라웠다. 이 프로젝트의 주요 기술이라 할 수 있겠다.   