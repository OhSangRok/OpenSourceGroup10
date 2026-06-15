-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: school_event_db
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `buildings`
--

DROP TABLE IF EXISTS `buildings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `buildings` (
  `building_id` int NOT NULL AUTO_INCREMENT,
  `building_name` varchar(100) NOT NULL,
  `latitude` decimal(10,7) DEFAULT NULL,
  `longitude` decimal(10,7) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`building_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `buildings`
--

LOCK TABLES `buildings` WRITE;
/*!40000 ALTER TABLE `buildings` DISABLE KEYS */;
INSERT INTO `buildings` VALUES (1,'체육관-공연예술센터',37.3194170,127.1326150,'체육관 및 공연예술센터'),(2,'인문관',37.3217310,127.1290900,'인문관 건물'),(3,'퇴계기념중앙도서관',37.3212000,127.1274200,'중앙도서관'),(4,'학군단',37.3188490,127.1314050,'학군단'),(5,'대운동장',37.3208080,127.1330960,'대운동장'),(6,'미술관',37.3197470,127.1309960,'미술관'),(7,'단국역사관',37.3195070,127.1300610,'단국역사관'),(8,'콘서트홀',37.3191830,127.1297850,'콘서트홀'),(9,'난파음악관',37.3187940,127.1292120,'난파음악관'),(10,'연민기념관',37.3180850,127.1284250,'연민기념관'),(11,'무용관',37.3159380,127.1273120,'무용관'),(12,'테니스장',37.3207400,127.1298290,'테니스장'),(13,'석주선기념박물관',37.3191700,127.1279080,'석주선 기념박물관'),(14,'평화의광장',37.3199770,127.1289750,'평화의 광장'),(15,'법학관-대학원동',37.3212230,127.1293780,'법학관-대학원동'),(16,'상경관',37.3223370,127.1289470,'상경관'),(17,'사범관',37.3228880,127.1290740,'사범관'),(18,'미디어센터',37.3223170,127.1276250,'미디어 센터'),(19,'소프트웨어 ICT관',37.3228360,127.1272690,'소프트웨어 ICT관'),(20,'범정관',37.3217810,127.1265270,'범정관'),(21,'복지관-죽전치과병원',37.3220890,127.1248940,'복지관-죽전치과병원'),(22,'글로컬 산학협력관',37.3219900,127.1237340,'글로컬 산학협력관'),(23,'사회과학관',37.3213680,127.1254160,'사회과학관'),(24,'제 1공학관',37.3209600,127.1258800,'제 1공학관'),(25,'제 2공학관',37.3205920,127.1263580,'제 2공학관'),(26,'제 3공학관',37.3202740,127.1268040,'제 3공학관'),(27,'혜당관',37.3204370,127.1283770,'혜당관'),(28,'종합실험동',37.3199260,127.1255670,'종합실험동'),(29,'국제관',37.3190340,127.1271810,'국제관'),(30,'노천마당',37.3197580,127.1274850,'노천마당');
/*!40000 ALTER TABLE `buildings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bus_schedules`
--

DROP TABLE IF EXISTS `bus_schedules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bus_schedules` (
  `schedule_id` int NOT NULL AUTO_INCREMENT,
  `stop_id` int DEFAULT NULL,
  `bus_number` varchar(50) DEFAULT NULL,
  `arrival_time` time DEFAULT NULL,
  `weekday_type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`schedule_id`),
  KEY `stop_id` (`stop_id`),
  CONSTRAINT `bus_schedules_ibfk_1` FOREIGN KEY (`stop_id`) REFERENCES `bus_stops` (`stop_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bus_schedules`
--

LOCK TABLES `bus_schedules` WRITE;
/*!40000 ALTER TABLE `bus_schedules` DISABLE KEYS */;
INSERT INTO `bus_schedules` VALUES (1,1,'24번','08:10:00','weekday'),(2,1,'24번','08:30:00','weekday'),(3,1,'720-3번','08:20:00','weekday'),(4,2,'810번','09:00:00','weekday'),(5,2,'810번','09:20:00','weekday'),(6,1,'24번','23:50:00','weekday');
/*!40000 ALTER TABLE `bus_schedules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bus_stops`
--

DROP TABLE IF EXISTS `bus_stops`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bus_stops` (
  `stop_id` int NOT NULL AUTO_INCREMENT,
  `stop_name` varchar(100) NOT NULL,
  `latitude` decimal(10,7) DEFAULT NULL,
  `longitude` decimal(10,7) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`stop_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bus_stops`
--

LOCK TABLES `bus_stops` WRITE;
/*!40000 ALTER TABLE `bus_stops` DISABLE KEYS */;
INSERT INTO `bus_stops` VALUES (1,'단국대.치과병원',37.3211000,127.1261000,'단국대학교 치과병원 앞 정류장'),(2,'단국대.종합실험동',37.3218000,127.1268000,'종합실험동 근처 정류장'),(3,'단국대.평화의광장',37.3225000,127.1275000,'평화의광장 근처 정류장'),(4,'단국대.인문관',37.3232000,127.1282000,'인문관 앞 정류장'),(5,'단국대정문',37.3240000,127.1290000,'단국대학교 정문 정류장'),(6,'단국대차고지',37.3250000,127.1300000,'단국대학교 차고지 정류장'),(7,'죽전역',NULL,NULL,'죽전역 셔틀버스 승차장');
/*!40000 ALTER TABLE `bus_stops` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events` (
  `event_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` text,
  `building_id` int DEFAULT NULL,
  `college` varchar(100) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `start_datetime` datetime DEFAULT NULL,
  `end_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`event_id`),
  KEY `building_id` (`building_id`),
  CONSTRAINT `events_ibfk_1` FOREIGN KEY (`building_id`) REFERENCES `buildings` (`building_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (1,'AI 세미나','AI 특강 진행',1,'소프트웨어융합대학','소프트웨어학과','2026-05-20 14:00:00','2026-05-20 16:00:00'),(2,'해커톤','팀 프로젝트 행사',2,'소프트웨어융합대학','컴퓨터공학과','2026-05-21 10:00:00','2026-05-21 18:00:00'),(3,'[교육혁신원 교수학습개발센터] AX 대응을 위한 교육과정 혁신방안, AX-EL Co-Creation Workshop 참여 교수자 모집','[교육혁신원 교수학습개발센터] AX 대응을 위한 교육과정 혁신방안, AX-EL Co-Creation Workshop 참여 교수자 모집\n\n\n[모집] 2026 AX-EL Co-Creation Workshop: AI로 설계하는 미래 교육의 여정\n안녕하세요, 교육혁신원 교수학습개발센터입니다.\n급변하는 AX(AI Transformation) 시대를 맞아, 우리 대학은 교수님들과 함께 학생들의 성공적인 성장을 지원하는\n미래지향적 학습 경험을 설계하고자 합니다. 이에 따라 교육 현장에 즉시 적용 가능한 AI 교수 전략을 도출하고,\n차세대 교육 모델을 공동 설계하는 ‘2026 AX-EL Co-creation Workshop’ 을 개최하오니 교수님들의 많은 관심과 참여를 부탁드립니다.\n첫 워크숍은 맞춤형 툴셋과 AI프롬프트를 활용해 교수님께서 직접 학과별 AI마이크로디그리를 기획하고\n구체적인 실행 로드맵을 수립하는 실무 중심의 집중 과정으로 운영됩니다.\n1. 워크숍 개요\n- 주제: AX 대응을 위한 교육과정 혁신방안\n- 일시 및 장소: (캠퍼스별 1일 선택 참여)\n[천안] 2026. 06. 24.(수) 13:00~17:00 | 율곡기념도서관 B1층 바이오헬스 디지털플래닛 내 텔레프레즌스 강의실\n[죽전] 2026. 06. 25.(목) 13:00~17:00 | 산학협력관 1층 글로컬산학협력관 세미나실(109호)\n- 참여 대상: AI 마이크로디그리 개설을 희망하는 학과 전임교원\n- 모집 인원: 캠퍼스별 총 30명 이내 (선착순 마감)\n2. 주요 프로그램 내용 (총 4시간)\n- AX 성숙도 및 동향 분석: 교육 분야 AX 사례 및 전공별 산업·직무 동향 분석 (외부 전문가 특강 포함)\n- 학생 중심 학습 여정 재설계: 입학부터 졸\n(선착순 마감)\n2. 주요 프로그램 내용 (총 4시간)\n- AX 성숙도 및 동향 분석: 교육 분야 AX 사례 및 전공별 산업·직무 동향 분석 (외부 전문가 특강 포함)\n- 학생 중심 학습 여정 재설계: 입학부터 졸업까지의 학생 페인포인트(Painpoint) 도출 및 개선 아이디어 제안\n- 미래 교육 설계: AI 마이크로디그리 신규 기획 및 AX형 강의계획/상세 교수전략 도출\n- 실행 로드맵 수립: 현장에 즉시 적용 가능한 90일 파일럿 실행 계획 수립\n3. 참여 교수님을 위한 혜택\n- 교원 교육업적평가 반영 : 참여 교수님 전원 반영\n- AI 관련 도서 증정 : 참여자 중 약 20명 추첨 지급\n- 생성형 AI 크레딧 제공 : 추첨을 통해 일부 참여 학과에 생성형 AI 크레딧 학생 계정 지급 (SW중심대학사업단 지원)\n4. 신청 방법\n- 신청 기한: [ 2026.06.16. 화요일 ] 까지\n- 신청 방법: 소속 단과대학 교학행정팀에 신청, 교학행정팀에서 수합하여 ‘업무연락’으로 회신, ※ 업무연락 회신 순서대로 접수\n- 문의: 교육혁신원 교수학습개발센터 지희정 연구교수(031-8005-2586)\n교수님께서 보유하신 학문적 전문성에 AI의 가능성을 더해,\n우리 학생들에게 더욱 풍부한 학습 경험을 제공할 수 있는 이번 기회에 꼭 함께해 주시길 바랍니다.\n단국대학교 교육혁신원 교수학습개발센터\n\n원문: https://www.dankook.ac.kr/web/kor/-390?p_p_id=dku_bbs_web_BbsPortlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_dku_bbs_web_BbsPortlet_cur=1&_dku_bbs_web_BbsPortlet_action=view_message&_dku_bbs_web_BbsPortlet_orderBy=createDate&_dku_bbs_web_BbsPortlet_bbsMessageId=175752',22,NULL,'RAG','2026-06-24 13:00:00','2026-06-24 14:00:00'),(4,'[창업지원단] 「모두의 창업 프로젝트」 도전자 모집 (사업설명회: 4월 22일 14시)','[창업지원단] 「모두의 창업 프로젝트」 도전자 모집 (사업설명회: 4월 22일 14시)\n\n\n? \'모두의 창업 프로젝트\' 도전자 등록\n⭕단국대학교 창업지원단은 혁신적인 창업 인재 양성을 위한 「모두의 창업 프로젝트」 운영기관으로 선정되었습니다!\n⭕ ‘모두의 창업’은 전국 단위 창업 프로젝트로, 창업 경험이 없어도 참여할 수 있으며 아이디어를 구체화하고 직접 시도해보며 발전시켜 나갈 수 있도록 단계별로 지원하는 프로그램입니다.\n⭕\'모두의 창업 프로젝트\'의 활동 이력이 창업자 개인의 경력으로 축적될 수 있도록 \'도전 경력증명서\'를 발행하며, 향후 창업지원사업에 참여할 경우 우대하고, 재학생의경우 영웅스토리 마일리지와 창업지원단장 명의의 참가확인서와 멘토링, 네트워킹 등을 지원할 예정입니다.\n⭕또한, 아이디어는 있지만 실행이 어려운 분들을 위해, ‘모두의 창업 프로젝트’ 설명회 와 함께 \'스타멘토\' 특강을 준비했습니다. 실제 창업 경험을 가진 스타 멘토의 이야기를 통해 창업의 힌트를 얻어보세요 !!\n↓↓↓모두의창업 참여 방법 ↓↓↓\n[1단계] 모두의 창업 설명회에 참여한다.\n-일시: 2026. 4. 22.(수) 14시 ~ 16시\n- 장소: 혜당관 학생극장\n- 참가신청: (학생) https://forms.gle/b3hBwpeXa8tQmELj6 * 참가신청 참여 시 참가확인서 발급 및 영웅스토리 마일리지 적립!!\n(지역주민 등) https://forms.gle/DacUmLr1TWRD4pJv7\n- 기타사항: 1:1 상담부스 운영 (로컬/일반 트랙)\n[2단계] 모두의창업 프로젝트 신청한다.\n- 기간: ~ 2026. 5. 15.(금) 16시까지\n- 신청방법: 모두의창업 플랫폼 접속 (www.modoo.or.kr)\n- 신청\n1:1 상담부스 운영 (로컬/일반 트랙)\n[2단계] 모두의창업 프로젝트 신청한다.\n- 기간: ~ 2026. 5. 15.(금) 16시까지\n- 신청방법: 모두의창업 플랫폼 접속 (www.modoo.or.kr)\n- 신청트랙: 일반/기술 트랙\n- 신청기관: 경기도 ->단국대\n[3단계] 모두의창업 프로젝트 신청완료 후 화면 캡처하여 영웅스토리에 신청한다! (학생 해당)\n?「모두의 창업 프로젝트」참여한 분들에게는 다음과 같은 특별한 혜택이 주어집니다.\n1️⃣ 1:1 창업 전문가 멘토링 지원\n2️⃣ 정부지원사업 연계 지원\n3️⃣ 선배 창업가 및 학내외 창업 네트워크 지원 등\n\n원문: https://www.dankook.ac.kr/web/kor/-390?p_p_id=dku_bbs_web_BbsPortlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_dku_bbs_web_BbsPortlet_cur=3&_dku_bbs_web_BbsPortlet_action=view_message&_dku_bbs_web_BbsPortlet_orderBy=createDate&_dku_bbs_web_BbsPortlet_bbsMessageId=171634',27,NULL,'RAG','2026-04-22 14:00:00','2026-04-22 15:00:00'),(5,'동양학연구원 제195회 정기연구발표회 개최','동양학연구원 제195회 정기연구발표회 개최\n\n\n단국대학교 동양학연구원에서는 아래와 같이 제195회 정기연구발표회를 진행합니다.\n제195회 동양학연구원 정기연구발표회\n일시 : 2026년 4월 16일 (목요일) 13:00~16:00\n장소 : 단국대학교 중앙도서관 세미나실(6-4호)\n주제 : AI 기반 한국 고대 종족의 문헌·고고학 자료의 통합 DB 구축 방법론\n사회 : 이종수(단국대학교 동양학연구원 역사문화연구소 소장)\n제1발표 : BERTopic을 활용한 중국 동북지역 선사시대 연구 동향 분석\n발표 : 김상훈(고려대학교)\n토론 : 정현승(단국대 석주선기념박물관)\n제2발표 : AI 기반 문헌·고고학 데이터의 통합적 분석 프레임워크 구축\n― 만주와 한반도 북부지역 고대 종족 자료를 중심으로 ―\n발표 : 오대양(단국대 동양학연구원)\n토론 : 조원진(한양대학교)\n참여를 원하시는 연구자께서는 아래의 당담자에게 미리 연락을 부탁드립니다.\n감사합니다.\n동양학연구원 연구전담조교수 오대양\n연구실 : 031-8005-3762\n핸드폰 : 010-6352-4348\n\n원문: https://www.dankook.ac.kr/web/kor/-390?p_p_id=dku_bbs_web_BbsPortlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_dku_bbs_web_BbsPortlet_cur=4&_dku_bbs_web_BbsPortlet_action=view_message&_dku_bbs_web_BbsPortlet_orderBy=createDate&_dku_bbs_web_BbsPortlet_bbsMessageId=170572',13,NULL,'RAG','2026-04-16 13:00:00','2026-04-16 14:00:00'),(6,'[창업지원단] 「모두의 창업 프로젝트」 도전자 모집 (~5/15, 16시까지)','[창업지원단] 「모두의 창업 프로젝트」 도전자 모집 (~5/15, 16시까지)\n\n\n단국대학교가 「모두의 창업 프로젝트」 운영기관으로 선정되었습니다‼️\n교내 모두의 창업 을 지원합니다 ?\n?신청방법: 모두의창업 플랫폼 →도전하기→지원서 작성→ 경기도 선택 →✨단국대학교(용인)✨ 선택!!\n?모두의창업 설명회\n(죽전) 2026. 4. 22.(수) 14:00 ~ 16:00 혜당관 학생극장\n(천안) 2026. 4. 9. (목) 12:00~13:00 인문과학관 B1층 디지털 리빙랩 시어터\n\n원문: https://www.dankook.ac.kr/web/kor/-390?p_p_id=dku_bbs_web_BbsPortlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_dku_bbs_web_BbsPortlet_cur=5&_dku_bbs_web_BbsPortlet_action=view_message&_dku_bbs_web_BbsPortlet_orderBy=createDate&_dku_bbs_web_BbsPortlet_bbsMessageId=170525',27,NULL,'RAG','2026-04-22 16:00:00','2026-04-22 17:00:00'),(7,'[한중관계연구소] 제21회 학술대회(2026.03.20.): 근현대 해외 유학 인물의 연구 방향과 전망','[한중관계연구소] 제21회 학술대회(2026.03.20.): 근현대 해외 유학 인물의 연구 방향과 전망\n\n\n제21회 단국대학교 부설 한중관계연구소 학술대회\n근현대 해외 유학 인물의 연구 방향과 전망\n한중관계연구소에서는 제21회 학술대회를 다음과 같이 개최하오니 관심있는 분들의 많은 참여를 바랍니다.\n일시 : 2026년 3월 20일 (금요일) 14:00~18:00\n장소 : 단국대학교 죽전캠퍼스 국제관 102호\n단국대학교 부설 한중관계연구소\n\n원문: https://www.dankook.ac.kr/web/kor/-390?p_p_id=dku_bbs_web_BbsPortlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_dku_bbs_web_BbsPortlet_cur=6&_dku_bbs_web_BbsPortlet_action=view_message&_dku_bbs_web_BbsPortlet_orderBy=createDate&_dku_bbs_web_BbsPortlet_bbsMessageId=166894',29,NULL,'RAG','2026-03-20 14:00:00','2026-03-20 15:00:00'),(8,'[한문교육연구소] 인문사회연구소 지원사업 제21회 한연포럼 개최 안내','[한문교육연구소] 인문사회연구소 지원사업 제21회 한연포럼 개최 안내\n\n\n한문교육연구소 제21회 한연포럼에 대해 안내 드립니다.\n이번 포럼은 콜로라도 대학 볼더 캠퍼스 아시아 언어문명학부 일본학과 Marjorie Burge 교수님을 모시고 ‘지도로 보는 고대 문자 문화’ 라는 주제로 강연이 진행될 예정입니다.\n자세한 일정은 다음과 같습니다.\n-강의 주제: 지도로 보는 고대 문자 문화 (Mapping \"Place\" in the Early Writen Cultures of Korea and Japan)\n-강의 일정: 2026.03.24.(화) 오전 10시 30분\n-강의 장소: 사범관 ZOOM 온라인\n(https://us06web.zoom.us/j/5451262790?pwd=ZnWXkzEbUNFurbO11CcSa0BAdJaWIB.1&omn=87165443345)\n-강사 소개: Marjorie Burge, 콜로라도 대학 볼더 캠퍼스 아시아 언어문명학부 일본학과 조교수\n어렵게 모신 만큼 많은 관심과 참여 부탁드립니다. 포럼 참가를 통해 유익한 정보와 인사이트를 얻어 가시길 바랍니다.\n감사합니다.\n\n원문: https://www.dankook.ac.kr/web/kor/-390?p_p_id=dku_bbs_web_BbsPortlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_dku_bbs_web_BbsPortlet_cur=6&_dku_bbs_web_BbsPortlet_action=view_message&_dku_bbs_web_BbsPortlet_orderBy=createDate&_dku_bbs_web_BbsPortlet_bbsMessageId=168234',17,NULL,'RAG','2026-03-24 10:30:00','2026-03-24 11:30:00'),(9,'[한문교육연구소] 인문사회연구소 지원사업 제7회 InDi 학술대회 개최 안내','[한문교육연구소] 인문사회연구소 지원사업 제7회 InDi 학술대회 개최 안내\n\n\n근역한문학회, 한문교육연구소 주최 제7회 InDi 학술대회 개최 안내합니다.\n●주제: AI시대 한문학 연구의 미래와 방향\n●일시: 2026년 3월 27(금) 13:00 ~ 17:30\n●장소: 단국대학교 죽전캠퍼스 글로컬산학협력관 B102호\n●주최: 근역한문학회, 단국대학교 한문교육연구소\n자세한 일정은 프로그램 안내문을 참고하시기 바랍니다. 많은 관심 부탁드립니다.\n감사합니다.\n\n원문: https://www.dankook.ac.kr/web/kor/-390?p_p_id=dku_bbs_web_BbsPortlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_dku_bbs_web_BbsPortlet_cur=6&_dku_bbs_web_BbsPortlet_action=view_message&_dku_bbs_web_BbsPortlet_orderBy=createDate&_dku_bbs_web_BbsPortlet_bbsMessageId=168235',22,NULL,'RAG','2026-03-27 13:00:00','2026-03-27 14:00:00'),(10,'[교육혁신원] 2025학년도 단국대학교 교육혁신원 성과포럼 안내','[교육혁신원] 2025학년도 단국대학교 교육혁신원 성과포럼 안내\n\n\n단국대학교 교육혁신원에서는 AI 대전환 시대를 맞아 우리 대학의 교육 혁신 성과를 공유하고 미래 비전을 논의하는\n? **「AX-EL INNOVATION FORUM 2025」** 를 개최합니다.\n미래형 교육 모델 AX-EL 과 인간 고유의 비판적 사고력을 보호하는 BREAK 모델을 통해 대학 교육의 새로운 지평을 열고자 합니다.\n?뇌과학과 AI가 만나는 혁신적인 통찰의 시간에 여러분을 초대합니다.\n대학 교육의 새로운 궤도를 함께 그려나갈 교수님, 학생, 연구자분들의 많은 관심과 참여를 부탁드립니다 !\n? 행사 개요\n●일시: 2026년 1월 30일(금) 13:30 ~ 17:00\n● 장소: 단국대학교 죽전캠퍼스 미디어센터 507호\n● 참여방법: 현장 참석 및 YouTube 실시간 생중계\n? 주요 링크\n[참가 신청하기]\nhttps://docs.google.com/forms/d/e/1FAIpQLSeAIX3__HgfpTc5jdawunJ_t-dIkV8hU2pqqYbynDVvOnxX_g/viewform\n(*사전신청을 하신 분들에게는 자료집을 보내드립니다.)\n[YouTube 실시간 중계 시청] https://www.youtube.com/live/nJFUyvinfX8\n(*현장 참여가 어려우신 분들은 온라인 라이브를 통해 함께하실 수 있습니다.)\n\n원문: https://www.dankook.ac.kr/web/kor/-390?p_p_id=dku_bbs_web_BbsPortlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_dku_bbs_web_BbsPortlet_cur=9&_dku_bbs_web_BbsPortlet_action=view_message&_dku_bbs_web_BbsPortlet_orderBy=createDate&_dku_bbs_web_BbsPortlet_bbsMessageId=165342',18,NULL,'RAG','2026-01-30 13:30:00','2026-01-30 14:30:00'),(11,'[마음건강연구소] 2026년도 마음건강연구소 동계 학술대회 개최 안내','[마음건강연구소] 2026년도 마음건강연구소 동계 학술대회 개최 안내\n\n\n2026 마음건강연구소 동계 학술대회 개최 안내\n단국대학교 부설 마음건강연구소에서는 다음과 같이 학술대회를 개최합니다.\n많은 관심과 참여 부탁드립니다.\n1. 행사 주제 : 심리학 연구를 위한 메타분석\n2. 행사 일시 : 2026.01.14.(수) 10:00 - 18:00\n3. 행사 장소 : 단국대학교 사회과학관 415호\n4. 행사 주최 : 마음건강연구소\n1부 메타분석\n2부 심리평가와 심리치료의 실제\n\n원문: https://www.dankook.ac.kr/web/kor/-390?p_p_id=dku_bbs_web_BbsPortlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_dku_bbs_web_BbsPortlet_cur=10&_dku_bbs_web_BbsPortlet_action=view_message&_dku_bbs_web_BbsPortlet_orderBy=createDate&_dku_bbs_web_BbsPortlet_bbsMessageId=164704',23,NULL,'RAG','2026-01-14 10:00:00','2026-01-14 11:00:00'),(12,'[단국대학교 산학협력단] 창업지원단 프로젝트 계약직(연구원) 모집 공고','[단국대학교 산학협력단] 창업지원단 프로젝트 계약직(연구원) 모집 공고\n\n\n[단국대학교 산학협력단] 창업지원단 프로젝트 계약직(연구원) 모집 공고\n1. 모집 분야 및 직무\n● 모집 분야: 단국대학교 산학협력단 스포츠산업 창업지원사업 프로젝트 계약직(행정연구원)\n● 담당 업무\n- 창업지원단 창업 지원사업 프로그램 기획 및 운영\n- 창업지원단 창업 기업 발굴, 육성 및 행정 지원\n- 창업지원단 사업비 집행 관리 및 정산, 성과 지표 관리\n● 모집인원 : 1명\n2. 근무 조건\n● 근무 장소: 단국대학교 창업지원단(죽전캠퍼스 글로컬산학협력관 303호)\n● 근무 시간: 주 5일(월~금), 09:00 ~ 17:00\n● 급여 조건 (세전 기준)\n- 연봉 3,000만원 수준 ※ 경력에 따라 호봉 산정(내부 기준에 따름)\n- 복리후생: 4대 보험(산학협력단) 적용, 퇴직금 지급(1년 이상 근무 시), 기타 내규에 따른 복리후생\n● 계약 기간: 2026. 6. 1. ~ 2026. 12. 31.\n* 산학협력단장이 필요하다고 인정할 경우 총 사업기간 내에 재계약할 수 있음\n3. 지원 자격 및 우대 사항\n● 지원 자격\n- 학사 학위 이상 소지자(2026년 8월 졸업예정자 포함)\n- 교육 공무원 임용에 결격 사유가 없는 자\n- 남자의 경우, 병역을 필한 자 또는 면제자\n- 단국대 창업생태계를 성장시킬 인재 누구나\n● 우대 사항\n- 정부 재정지원 사업(국책사업) 행정 및 정산 업무 경험자\n- 오피스 활용 우수자\n4. 채용일정 및 방법\n● 채용일정\n공고 및 접수\n\n원문: https://www.dankook.ac.kr/web/kor/apply_noti?p_p_id=dku_bbs_web_BbsPortlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_dku_bbs_web_BbsPortlet_cur=2&_dku_bbs_web_BbsPortlet_action=view_message&_dku_bbs_web_BbsPortlet_orderBy=createDate&_dku_bbs_web_BbsPortlet_bbsMessageId=174513',22,NULL,'RAG','2026-06-01 09:00:00','2026-06-01 10:00:00'),(13,'[단국대학교 산학협력단] 창업지원단 프로젝트 계약직(연구원) 모집 공고','[단국대학교 산학협력단] 창업지원단 프로젝트 계약직(연구원) 모집 공고\n\n\n[ 단국대학교 산학협력단 ] 창업지원단 프로젝트 계약직 ( 연구원 ) 모집 공고\n1. 모집 분야 및 직무\n● 모집 분야 : 단국대학교 산학협력단 스포츠산업 창업지원사업 프로젝트 계약직 ( 행정연구원 )\n● 담당 업무\n- 창업지원단 창업 지원사업 프로그램 기획 및 운영\n- 창업지원단 창업 기업 발굴 , 육성 및 행정 지원\n- 창업지원단 사업비 집행 관리 및 정산 , 성과 지표 관리\n● 모집인원 : 2 명\n2. 근무 조건\n● 근무 장소 : 단국대학교 창업지원단 ( 죽전캠퍼스 글로컬산학협력관 303 호 )\n● 근무 시간 : 주 5 일 ( 월 ~ 금 ), 09:00 ~ 17:00\n● 급여 조건 ( 세전 기준 )\n- 연봉 3,000 만원 수준 ※ 경력에 따라 호봉 산정 ( 내부 기준에 따름 )\n- 복리후생 : 4 대 보험 ( 산학협력단 ) 적용 , 퇴직금 지급 (1 년 이상 근무 시 ), 기타 내규에 따른 복리후생\n● 계약 기간 : 2026. 5. 1. ~ 2027. 3. 31.\n* 산학협력단장이 필요하다고 인정할 경우 총 사업기간 내에 재계약할 수 있음\n3. 지원 자격 및 우대 사항\n● 지원 자격\n- 학사 학위 이상 소지자 (2026 년 8 월 졸업예정자 포함 )\n- 교육 공무원 임용에 결격 사유가 없는 자\n- 남자의 경우 , 병역을 필한 자 또는 면제자\n- 단국대 창업생태계를 성장시킬 인재 누구나\n● 우대 사항\n- 정부 재정지원 사업 ( 국책사업 ) 행정 및 정산 업무 경험자\n- 오피스 활용 우수자\n4. 채용일정 및 방법\n● 채용일정\n공고 및 접수\n\n원문: https://www.dankook.ac.kr/web/kor/apply_noti?p_p_id=dku_bbs_web_BbsPortlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_dku_bbs_web_BbsPortlet_cur=3&_dku_bbs_web_BbsPortlet_action=view_message&_dku_bbs_web_BbsPortlet_orderBy=createDate&_dku_bbs_web_BbsPortlet_bbsMessageId=172822',22,NULL,'RAG','2026-05-01 09:00:00','2026-05-01 10:00:00'),(14,'[죽전] 프리무스국제대학 글로벌기초교육학부 학사조교 채용 공고(3월 임용)','[죽전] 프리무스국제대학 글로벌기초교육학부 학사조교 채용 공고(3월 임용)\n\n\n프리무스국제대학 글로벌기초교육학부에서 학사조교를 채용하고자 하오니 많은 지원 바랍니다 .\n■ 프리무스국제대학 글로벌기초교육학부 : 외국인 유학생 전용 학부로 , 소속 학생들은 입학 후 1 학년 동안 한국어 교과목 및 전공 기초과목을 이수합니다 . 외국인 유학생의 학사 생활을 지원하고 , 학교 적응을 돕는 업무를 담당할 조교를 모집합니다 .\n1. 모집 분야 및 지원 자격\n가 . 모집 분야 : 단국대학교 프리무스국제대학 글로벌기초교육학부 학사조교\n나 . 모집 인원 : 1 명\n다 . 담당 업무 : 학부 행정업무 및 외국인 유학생 학사관리\n라 . 공통 지원 자격\n1) 학사 졸업자 이상 (2026.2 월 졸업예정자 지원가능 )\n2) 조교 임용 절차에 결격 사유가 없는 자\n마 . 우대 사항 : 영어 또는 중국어 의사소통 능력 보유자 우대\n2. 근무 조건\n가 . 계약 기간 : 1 년 계약 (1 년 연장 가능 )\n나 . 근무 시작 : 2026년 3 월 임용 예정\n다 . 근무 시간 : 월 ~ 금 09:00~17:00 ( 점심시간 12:00~13:00)\n- 방학 기간 단축근무 운영 (09:00~15:00)\n라 . 급여 : 단국대학교 급여 기준 적용\n마 . 근무지 : 국제관 302 호 ( 프리무스국제대학 교학행정팀 )\n3. 전형 절차\n가 . 1 차 : 서류심사\n나 . 2 차 : 면접심사 (ZOOM 으로 진행 )\n- 면접 심사 상세 일정은 1 차 합격자에 한하여 개별 안내\n4. 제출 서류\n가 . 자기소개서 1 부 ( 첨부 양식 )\n나 . 이력서 1 부 ( 첨부 양식 )\n다 . 학부 졸업 ( 예정 ) 증명서 1 부\n라 . 학부 성적증명\n심사 상세 일정은 1 차 합격자에 한하여 개별 안내\n4. 제출 서류\n가 . 자기소개서 1 부 ( 첨부 양식 )\n나 . 이력서 1 부 ( 첨부 양식 )\n다 . 학부 졸업 ( 예정 ) 증명서 1 부\n라 . 학부 성적증명서 1 부\n5. 제출기한 및 방법\n가 . 제출기한 : 2026. 2.3.(화 ) 자정\n나 . 제출방법 : mkdl@dankook.ac.kr 로 제출서류 송부\n1) 메일 제목 : “ 글로벌기초교육학부 조교지원 ( 이름 )” 형식\n2) 모든 제출서류는 PDF 파일로 제출 ( 제출서류 : 4 번 목록 참고 )\n6. 기타 사항\n가 . 제출서류는 일체 반환하지 않습니다 .\n나 . 별도의 불합격 통보는 없습니다 .\n다 . 면접 일정은 1 차 서류 전형 합격자에 한하여 개별 통보합니다 .\n라 . 기타 문의 : 프리무스국제대학 교학행정팀 (031-8005-2292 )\n\n원문: https://www.dankook.ac.kr/web/kor/apply_noti?p_p_id=dku_bbs_web_BbsPortlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_dku_bbs_web_BbsPortlet_cur=8&_dku_bbs_web_BbsPortlet_action=view_message&_dku_bbs_web_BbsPortlet_orderBy=createDate&_dku_bbs_web_BbsPortlet_bbsMessageId=164840',29,NULL,'RAG','2026-02-03 09:00:00','2026-02-03 10:00:00'),(15,'[(죽전) 공과대학 토목환경공학과] 학사조교 모집 안내 (3월 임용)','[(죽전) 공과대학 토목환경공학과] 학사조교 모집 안내 (3월 임용)\n\n\n공과대학 토목환경공학과에서는 학사조교를 다음과 같이 모집하고 있으니 많은 지원바랍니다.\n1. 모집분야 및 지원 자격\n가. 모집분야 : 토목환경공학과 학사조교A (대학원 재학생) / 학사조교B (4년제 졸업이상)\n나. 모집인원 : 1명\n다. 지원자격(공통) : 4년제 대학 졸업자 및 학사학위자\n교육공무원 임용에 결격 사유가 없는 자\n남자는 병역을 필한 자 또는 면제자 우대\n2. 근무조건\n가. 근무기간 : 2026.03.02 ~ 2027.02.28. 1년 (1년 연장하여 최대 2년 가능)\n나. 근무시간 : 평일 09:00-17:00 (방학 중 15시 퇴근 주간 운영)\n다. 근무지: 죽전캠퍼스 제 1공학관 214호\n라. 담당업무 : 토목환경공학과 예산 및 대학원관련 업무 등\n마. 급여 : 단국대학교 급여기준에 따름.\n3. 전형방법\n서류 및 면접\n4. 제출서류\n1) 이력서 1부(사진 반드시 첨부)\n2) 졸업증명서 1부\n3) 그 외 경력증명서(선택)\n* 이력서 별도 양식 없음\n5. 제출기한 : 2026년 1월 30일 (금) 15:00까지\n6. 제출방법(택일)\n1) 방문접수 : 토목환경공학과 사무실 (죽전캠퍼스 제1공학관 2층 214호)\n평일 09:00-12:00 / 13:00-15:00\n2) 온라인접수 : 이메일 접수 (12240825a@dankook.ac.kr)\n* 온라인 접수 시 유의 사항 *\n- 메일 제목 : \"토목환경공학과 학사조교 지원자 OOO\"\n* 제출서류는 반환되지 않으며 별도의 불합격 통보는 없습니다.\n* 면접일정은 서류 전형 합격자에 한하여 개별통보(유선통보)합니다.\n* 근무 시작 예정일은 2026년 3월 2일이며, 출근 전 주에 인수인계를 반드시 받아야\n출서류는 반환되지 않으며 별도의 불합격 통보는 없습니다.\n* 면접일정은 서류 전형 합격자에 한하여 개별통보(유선통보)합니다.\n* 근무 시작 예정일은 2026년 3월 2일이며, 출근 전 주에 인수인계를 반드시 받아야 합니다.\n* 문의처 : 토목환경공학과 학과사무실 (031-8005-3470)\n- 공과대학 토목환경공학과 -\n\n원문: https://www.dankook.ac.kr/web/kor/apply_noti?p_p_id=dku_bbs_web_BbsPortlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_dku_bbs_web_BbsPortlet_cur=9&_dku_bbs_web_BbsPortlet_action=view_message&_dku_bbs_web_BbsPortlet_orderBy=createDate&_dku_bbs_web_BbsPortlet_bbsMessageId=164719',24,NULL,'RAG','2026-03-02 09:00:00','2026-03-02 10:00:00'),(16,'단국대학교 석주선기념박물관 2026년 매장유산 미정리유물 보존 및 활용사업 보조원(시간제) 채용 공고(~1/25(일) 17:00까지)','단국대학교 석주선기념박물관 2026년 매장유산 미정리유물 보존 및 활용사업 보조원(시간제) 채용 공고(~1/25(일) 17:00까지)\n\n\n[2026년 매장유산 미정리 유물 보존 및 활용 사업]과 관련하여 유물 정리 보조원을 다음과 같이 공개모집하오니 관심 있는 분들의 많은 지원을 바랍니다.\n가. 채용분야\n근무지\n\n원문: https://www.dankook.ac.kr/web/kor/apply_noti?p_p_id=dku_bbs_web_BbsPortlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_dku_bbs_web_BbsPortlet_cur=9&_dku_bbs_web_BbsPortlet_action=view_message&_dku_bbs_web_BbsPortlet_orderBy=createDate&_dku_bbs_web_BbsPortlet_bbsMessageId=165323',13,NULL,'RAG','2026-01-25 17:00:00','2026-01-25 18:00:00'),(17,'단국대학교 석주선기념박물관 2026년 매장유산 미정리유물 보존 및 활용사업 보조원(전문인력) 채용 공고(~1/25(일) 17:00까지)','단국대학교 석주선기념박물관 2026년 매장유산 미정리유물 보존 및 활용사업 보조원(전문인력) 채용 공고(~1/25(일) 17:00까지)\n\n\n[2026년 매장유산 미정리 유물 보존 및 활용 사업]과 관련하여 유물 정리 보조원을 다음과 같이 공개모집하오니 관심 있는 분들의 많은 지원을 바랍니다.\n가. 채용분야\n근무지\n\n원문: https://www.dankook.ac.kr/web/kor/apply_noti?p_p_id=dku_bbs_web_BbsPortlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_dku_bbs_web_BbsPortlet_cur=9&_dku_bbs_web_BbsPortlet_action=view_message&_dku_bbs_web_BbsPortlet_orderBy=createDate&_dku_bbs_web_BbsPortlet_bbsMessageId=165324',13,NULL,'RAG','2026-01-25 17:00:00','2026-01-25 18:00:00'),(18,'[죽전] 프리무스국제대학 글로벌기초교육학부 학사조교 채용 공고(2월 임용)','[죽전] 프리무스국제대학 글로벌기초교육학부 학사조교 채용 공고(2월 임용)\n\n\n프리무스국제대학 글로벌기초교육학부에서 학사조교를 채용하고자 하오니 많은 지원 바랍니다.\n■ 프리무스국제대학 글로벌기초교육학부: 외국인 유학생 전용 학부로, 소속 학생들은 입학 후 1학년 동안 한국어 교과목 및 전공 기초과목을 이수합니다. 외국인 유학생의 학사 생활을 지원하고, 학교 적응을 돕는 업무를 담당할 조교를 모집합니다.\n1. 모집 분야 및 지원 자격\n가. 모집 분야: 단국대학교 프리무스국제대학 글로벌기초교육학부 학사조교\n나. 모집 인원: 1명\n다. 담당 업무: 학부 행정업무 및 외국인 유학생 학사관리\n라. 공통 지원 자격\n1) 학사 졸업자 이상\n2) 조교 임용 절차에 결격 사유가 없는 자\n마. 우대 사항: 영어 또는 중국어 의사소통 능력 보유자 우대\n2. 근무 조건\n가. 계약 기간: 1년 계약(1년 연장 가능)\n나. 근무 시작: 2026. 2. 2.(월)\n다. 근무 시간: 월~금 09:00~17:00 (점심시간 12:00~13:00)\n- 방학 기간 단축근무 운영(09:00~15:00)\n라. 급여: 단국대학교 급여 기준 적용\n마. 근무지: 국제관 302호(프리무스국제대학 교학행정팀)\n3. 전형 절차\n가. 1차: 서류심사\n나. 2차: 면접심사(온라인 ZOOM 진행, 1.6.(화) 예정)\n- 면접 심사 상세 일정은 1차 합격자에 한하여 개별 안내\n4. 제출 서류\n가. 자기소개서 및 이력서 1부(첨부 양식)\n나. 학부 졸업증명서 1부\n다. 학부 성적증명서 1부\n5. 제출기한 및 방법\n가. 제출기한: 2026. 1. 3.(토)까지\n나. 제출방법: mkdl@dankook.ac.kr 로 제출서류 송부\n1) 메일 제목: “글로벌기초교육학부 조교지원(이름\n다. 학부 성적증명서 1부\n5. 제출기한 및 방법\n가. 제출기한: 2026. 1. 3.(토)까지\n나. 제출방법: mkdl@dankook.ac.kr 로 제출서류 송부\n1) 메일 제목: “글로벌기초교육학부 조교지원(이름)” 형식\n2) 모든 제출서류는 PDF 파일로 제출\n6. 기타 사항\n가. 제출서류는 일체 반환하지 않습니다.\n나. 합격/불합격 결과 및 안내사항은 이메일로 통보합니다.\n다. 기타 문의: 프리무스국제대학 교학행정팀(031-8005-2292)\n\n원문: https://www.dankook.ac.kr/web/kor/apply_noti?p_p_id=dku_bbs_web_BbsPortlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_dku_bbs_web_BbsPortlet_cur=10&_dku_bbs_web_BbsPortlet_action=view_message&_dku_bbs_web_BbsPortlet_orderBy=createDate&_dku_bbs_web_BbsPortlet_bbsMessageId=163114',29,NULL,'RAG','2026-02-02 09:00:00','2026-02-02 10:00:00'),(19,'2026.03.01.자 신규직원(정규직) 채용 실무평가 안내(AI역량검사, 실무면접, 전공시험)','2026.03.01.자 신규직원(정규직) 채용 실무평가 안내(AI역량검사, 실무면접, 전공시험)\n\n\n단국대학교 신규직원채용\n실무평가 안내\n⚠ 필독 : 응시 유의사항\n실무평가전형은 ①AI역량검사, ②실무면접, ③전공시험(해당자)으로 구성되며,\n하나의 시험이라도 미응시할 경우 불합격 처리 됩니다.\n1. AI 역량검사\n대상자 : 지원자 전체\n응시기간 : 2025.12.29(월) 15:00 ~ 12.31(수) 17:00\n응시방법 : 온라인 응시 페이지 접속 (기한 내 응시 필수)\n안내메일 : 2025.12.29(월) 15:00 발송 예정\n(※ 응시사이트, 로그인 정보 등 상세 내용 포함)\n[문의처] 시스템 오류 등 문의는 시행사로 연락 바랍니다.\n마이더스인 카카오톡 채널 바로가기\n2. 전공시험\n대상자 : 네트워크 분야 지원자\n일시 : 2026.01.03(토) 10:00 ~ 11:00 (60분)\n내용 : 전산전공 관련 문제 (20문제 내외)\n장소 : 단국대학교 죽전캠퍼스 사회과학관 101호 (하단 약도 참조)\n3. 실무면접\n장소 : 단국대학교 죽전캠퍼스 315호 회의실\n준비물 : 신분증(모바일 불가), 단정한 복장\n지원 분야\n\n원문: https://www.dankook.ac.kr/web/kor/apply_noti?p_p_id=dku_bbs_web_BbsPortlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_dku_bbs_web_BbsPortlet_cur=10&_dku_bbs_web_BbsPortlet_action=view_message&_dku_bbs_web_BbsPortlet_orderBy=createDate&_dku_bbs_web_BbsPortlet_bbsMessageId=163116',23,NULL,'RAG','2026-03-01 15:00:00','2026-03-01 16:00:00'),(20,'[죽전] 자유교양대학 교학행정1팀 학사조교 채용 공고(26년 2월 임용)','[죽전] 자유교양대학 교학행정1팀 학사조교 채용 공고(26년 2월 임용)\n\n\n[자유교양대학 학사조교 채용 공고 ]\n1. 모집분야 및 지원 자격\n가. 모집분야 : 자유교양대학 교학행정1팀 학사조교\n나. 모집인원 : 1명\n다. 지원자격(공통)\n1) 4년제 대학 졸업자\n2) 조교 임용에 결격 사유가 없는 자\n2. 근무조건\n가. 계약기간 : 1년(1년 연장가능) / 근무시작 2026.02.01\n나. 근무시간 : 월-금 09:00-17:00(점심시간 12:00~13:00) / 단축근무 기간 09:00~15:00\n다. 담당업무 : 자유교양대학 학사 및 행정 업무 지원\n라. 급 여 : 단국대학교 급여기준에 따름\n마. 근 무 지 : 사범관 308호 교학행정팀\n3. 전형방법\n가. 1차 서류심사\n나. 2차 면접심사(일정 추후 개별통보)\n4. 제출서류(자유양식)\n가. 이력서(증명사진 첨부)\n나. 자기소개서\n다. 졸업증명서\n라. 성적증명서\n5. 제출기한 및 방법\n가. 제출기한 : 2026년 01월 08일(목) 자정까지\n나. 제출방법 : 이메일 접수 (12241200k@dankook.ac.k)\n1) 메일제목 : \"자유교양대학 조교 지원 이름 000\"\n2) 첨부파일 : ①이력서(성명) ②자기소개서(성명) ③졸업증명서(성명) ④성적증명서(성명)\n6. 기타사항\n가. 면접 일정은 1차 서류합격자에 한하여 개별 통보(유선)하며, 불합격자에 대한 별도의 통보는 하지 않습니다.\n나. 제출한 서류는 반환하지 않으며, 채용절차 종료 이후 자체적으로 폐기합니다.\n다. 문의사항은 자유교양대학 교학행정팀(031-8005-2522)으로 연락 바랍니다.\n자 유 교 양 대 학 장\n\n원문: https://www.dankook.ac.kr/web/kor/apply_noti?p_p_id=dku_bbs_web_BbsPortlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_dku_bbs_web_BbsPortlet_cur=10&_dku_bbs_web_BbsPortlet_action=view_message&_dku_bbs_web_BbsPortlet_orderBy=createDate&_dku_bbs_web_BbsPortlet_bbsMessageId=163415',17,NULL,'RAG','2026-02-01 09:00:00','2026-02-01 10:00:00');
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `favorite_events`
--

DROP TABLE IF EXISTS `favorite_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favorite_events` (
  `favorite_id` int NOT NULL AUTO_INCREMENT,
  `student_id` varchar(20) NOT NULL,
  `event_id` int NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`favorite_id`),
  UNIQUE KEY `student_id` (`student_id`,`event_id`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `favorite_events_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`student_id`),
  CONSTRAINT `favorite_events_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorite_events`
--

LOCK TABLES `favorite_events` WRITE;
/*!40000 ALTER TABLE `favorite_events` DISABLE KEYS */;
/*!40000 ALTER TABLE `favorite_events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personal_schedules`
--

DROP TABLE IF EXISTS `personal_schedules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personal_schedules` (
  `schedule_id` int NOT NULL AUTO_INCREMENT,
  `student_id` varchar(20) NOT NULL,
  `title` varchar(100) NOT NULL,
  `schedule_date` date NOT NULL,
  `schedule_time` time DEFAULT NULL,
  `building_id` int DEFAULT NULL,
  `memo` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`schedule_id`),
  KEY `student_id` (`student_id`),
  KEY `building_id` (`building_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personal_schedules`
--

LOCK TABLES `personal_schedules` WRITE;
/*!40000 ALTER TABLE `personal_schedules` DISABLE KEYS */;
/*!40000 ALTER TABLE `personal_schedules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shuttle_schedules`
--

DROP TABLE IF EXISTS `shuttle_schedules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shuttle_schedules` (
  `schedule_id` int NOT NULL AUTO_INCREMENT,
  `stop_id` int DEFAULT NULL,
  `shuttle_time` time DEFAULT NULL,
  PRIMARY KEY (`schedule_id`),
  KEY `shuttle_schedules_ibfk_1` (`stop_id`),
  CONSTRAINT `shuttle_schedules_ibfk_1` FOREIGN KEY (`stop_id`) REFERENCES `bus_stops` (`stop_id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shuttle_schedules`
--

LOCK TABLES `shuttle_schedules` WRITE;
/*!40000 ALTER TABLE `shuttle_schedules` DISABLE KEYS */;
INSERT INTO `shuttle_schedules` VALUES (16,1,'08:30:00'),(17,2,'08:35:00'),(18,3,'08:37:00'),(19,4,'08:40:00'),(20,5,'08:43:00'),(26,7,'08:30:00'),(27,5,'08:35:00'),(28,4,'08:37:00'),(29,3,'08:40:00'),(30,2,'08:43:00'),(31,5,'16:00:00'),(32,5,'21:00:00');
/*!40000 ALTER TABLE `shuttle_schedules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shuttle_stops`
--

DROP TABLE IF EXISTS `shuttle_stops`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shuttle_stops` (
  `stop_id` int NOT NULL AUTO_INCREMENT,
  `stop_name` varchar(50) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`stop_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shuttle_stops`
--

LOCK TABLES `shuttle_stops` WRITE;
/*!40000 ALTER TABLE `shuttle_stops` DISABLE KEYS */;
INSERT INTO `shuttle_stops` VALUES (1,'죽전역','죽전역 셔틀버스 승차장'),(2,'죽전역','죽전역 셔틀버스 승차장'),(3,'정문','단국대학교 정문 셔틀버스 정류장'),(4,'인문관','인문관 셔틀버스 정류장'),(5,'평화의광장','평화의광장 셔틀버스 정류장'),(6,'종합실험동','종합실험동 셔틀버스 정류장');
/*!40000 ALTER TABLE `shuttle_stops` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `student_id` varchar(20) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `name` varchar(50) NOT NULL,
  `college` varchar(50) NOT NULL,
  `department` varchar(50) NOT NULL,
  `grade` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_admin` tinyint DEFAULT '0',
  PRIMARY KEY (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('32253449','$2b$12$IjISqKx9ZfJNFlAyjMEqP.hutEw4b2zrYrAMgovIuSW8y2Z6kqo5G','이윤형','AI 융합대학','소프트웨어학과',2,'2026-05-11 06:30:32',1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-16  2:05:51
