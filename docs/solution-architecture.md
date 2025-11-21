# Kumbuk Solution Architecture

## Business Problem Summary
**Core Problem**: In Sri Lanka, finding reliable local services and accessing community information is fragmented and difficult, while local service providers struggle with visibility and credibility.

**Target Users**: 
- Consumers seeking trusted local services
- Local service providers wanting to reach customers
- Community members needing local information

## High-Level Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                               KUMBUK ECOSYSTEM                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │   CONSUMER APP  │    │   PROVIDER APP  │    │   ADMIN PANEL   │        │
│  │ (React Native   │    │ (React Native   │    │   (React Web)   │        │
│  │  with Expo Go)  │    │  with Expo Go)  │    │                 │        │
│  └─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘        │
│           │                      │                      │                │
│           └──────────────────────┼──────────────────────┘                │
│                                  │                                         │
│  ════════════════════════════════╪═══════════════════════════════════════  │
│                                  │                                         │
│  ┌───────────────────────────────▼───────────────────────────────────────┐ │
│  │                    API GATEWAY LAYER                                   │ │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐   │ │
│  │  │  FastAPI Server │    │   Node.js/      │    │   SpringBoot    │   │ │
│  │  │  (Python +      │    │   Express.js    │    │   (Java)        │   │ │
│  │  │   Unicorn)      │    │                 │    │                 │   │ │
│  │  └─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘   │ │
│  └─────────────┼──────────────────────┼──────────────────────┼───────────┘ │
│               │                      │                      │             │
│  ┌─────────────▼──────────────────────▼──────────────────────▼───────────┐ │
│  │                    AGENTIC AI ORCHESTRATION LAYER                     │ │
│  │  ┌───────────────────────────────────────────────────────────────────┐ │ │
│  │  │              ORCHESTRATION AGENT (Main AI Coordinator)            │ │ │
│  │  │                     (LangChain + Vertex AI)                       │ │ │
│  │  │  ┌─────────────────────────┐  ┌─────────────────────────────────┐ │ │ │
│  │  │  │    SERVICE MATCHING     │  │      COMMUNITY INTELLIGENCE     │ │ │ │
│  │  │  │        AGENT            │  │           AGENT                 │ │ │ │
│  │  │  │  - Provider Discovery   │  │  - Local Event Processing      │ │ │ │
│  │  │  │  - Smart Ranking        │  │  - Community Insights          │ │ │ │
│  │  │  │  - Trust Assessment     │  │  - Notification Optimization   │ │ │ │
│  │  │  └─────────────────────────┘  └─────────────────────────────────┘ │ │ │
│  │  └───────────────────────────────────────────────────────────────────┘ │ │
│  └─────────────┬───────────────────────────────────────────────────────────┘ │
│               │                                                             │
│  ┌─────────────▼───────────────────────────────────────────────────────────┐ │
│  │                        DATA & STORAGE LAYER                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │ │
│  │  │  Firebase   │  │   Neo4j     │  │  PostgreSQL │  │   Redis     │   │ │
│  │  │ (Auth +     │  │ (Ontology & │  │(Relational  │  │  (Cache &   │   │ │
│  │  │ Real-time)  │  │ Knowledge   │  │    Data)    │  │  Sessions)  │   │ │
│  │  │             │  │   Graph)    │  │             │  │             │   │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Detailed Architecture Components

### 1. FRONTEND LAYER

#### A. Consumer Mobile App (React Native + Expo Go)
```
┌─────────────────────────────────────────────────────────────┐
│                    CONSUMER APP ARCHITECTURE                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    UI LAYER                             │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │Auth Screens │ │Search & List│ │Profile Mgmt │      │ │
│  │  │- Register   │ │- Categories │ │- Settings   │      │ │
│  │  │- Login      │ │- Providers  │ │- Location   │      │ │
│  │  │- PDPA       │ │- Details    │ │- Preferences│      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  │                                                         │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │Communication│ │Community    │ │Agentic UI   │      │ │
│  │  │- Call Now   │ │- Feed       │ │- AI Insights│      │ │
│  │  │- Inquiries  │ │- Events     │ │- Smart Recs │      │ │
│  │  │- Contact    │ │- Notices    │ │- Personalize│      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                  STATE MANAGEMENT                       │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │User Context │ │Search State │ │AI State     │      │ │
│  │  │- Profile    │ │- Filters    │ │- Preferences│      │ │
│  │  │- Auth Token │ │- Results    │ │- Insights   │      │ │
│  │  │- Location   │ │- Categories │ │- Learning   │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                  API SERVICE LAYER                      │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │Auth Service │ │FastAPI      │ │AI Service   │      │ │
│  │  │- Firebase   │ │- REST APIs  │ │- Agent Comm │      │ │
│  │  │- JWT Tokens │ │- Real-time  │ │- Insights   │      │ │
│  │  │- Session    │ │- Caching    │ │- Learning   │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Key Features Solving Business Problems:**
- **Discovery Solution**: Easy category-based browsing eliminates manual searching
- **Trust Building**: Verification badges and "Top Picks" build confidence
- **Speed**: One-tap calling and simple inquiry forms save time
- **Local Focus**: Location-based filtering shows only relevant services

#### B. Service Provider Mobile App (React Native + Expo)
```
┌─────────────────────────────────────────────────────────────┐
│                 SERVICE PROVIDER APP ARCHITECTURE           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    UI LAYER                             │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │Auth & Setup │ │Business Mgmt│ │Inquiry Mgmt │      │ │
│  │  │- Register   │ │- Profile    │ │- Inbox      │      │ │
│  │  │- Verification│ │- Services   │ │- Responses  │      │ │
│  │  │- Onboarding │ │- Categories │ │- History    │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  │                                                         │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │Analytics    │ │Agentic Help │ │Settings     │      │ │
│  │  │- Views      │ │- Profile    │ │- Notifications│    │ │
│  │  │- Inquiries  │ │- Tips       │ │- Privacy    │      │ │
│  │  │- Performance│ │- Suggestions│ │- Support    │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Key Features Solving Business Problems:**
- **Visibility Solution**: Easy profile creation gets providers online quickly
- **Credibility Building**: Verification system and profile completion guidance
- **Lead Management**: Centralized inquiry system replaces scattered communications
- **Growth Support**: Analytics and agentic tips help improve business

#### C. Admin Web Panel (React/Firebase Hosting)
```
┌─────────────────────────────────────────────────────────────┐
│                     ADMIN PANEL ARCHITECTURE                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                  MANAGEMENT INTERFACE                    │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │User Mgmt    │ │Provider Mgmt│ │Content Mgmt │      │ │
│  │  │- View Users │ │- Verification│ │- Community  │      │ │
│  │  │- Suspend    │ │- Approval   │ │- Events     │      │ │
│  │  │- Analytics  │ │- Categories │ │- Announcements│    │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  │                                                         │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │System Mgmt  │ │Analytics    │ │Support      │      │ │
│  │  │- Locations  │ │- Usage Stats│ │- Reports    │      │ │
│  │  │- Categories │ │- Performance│ │- Issues     │      │ │
│  │  │- Settings   │ │- Trends     │ │- Feedback   │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Key Features Solving Business Problems:**
- **Trust Management**: Manual verification ensures service quality
- **Community Building**: Content management keeps information current
- **Quality Control**: User and provider management maintains standards

### 2. BACKEND LAYER

#### A. Multi-Service Backend Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND SERVICES ARCHITECTURE            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                 PRIMARY API LAYER                       │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │  FastAPI    │ │  Node.js    │ │ SpringBoot  │      │ │
│  │  │  (Python)   │ │ Express.js  │ │   (Java)    │      │ │
│  │  │- Main APIs  │ │- Real-time  │ │- Enterprise │      │ │
│  │  │- ML/AI      │ │- WebSocket  │ │- Batch Proc │      │ │
│  │  │- Unicorn    │ │- Socket.io  │ │- Security   │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │               AUTHENTICATION & SECURITY                 │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │Firebase Auth│ │JWT Manager  │ │OAuth2/OIDC  │      │ │
│  │  │- Identity   │ │- Tokens     │ │- Third Party│      │ │
│  │  │- Sessions   │ │- Refresh    │ │- Security   │      │ │
│  │  │- Roles      │ │- Validation │ │- Compliance │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                  SERVICE MESH                           │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │Load Balancer│ │API Gateway  │ │Rate Limiting│      │ │
│  │  │- Nginx/HAP  │ │- Routing    │ │- Throttling │      │ │
│  │  │- SSL/TLS    │ │- Auth       │ │- Quotas     │      │ │
│  │  │- Health     │ │- Validation │ │- Monitoring │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### B. Advanced Agentic AI System (LangChain + Vertex AI + Neo4j)
```
┌─────────────────────────────────────────────────────────────┐
│              AGENTIC AI ORCHESTRATION ARCHITECTURE          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │            ORCHESTRATION AGENT (Main Coordinator)       │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │                 LangChain Framework                 │ │ │
│  │  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │ │ │
│  │  │  │Agent Memory │ │Task Planning│ │Decision Tree│   │ │ │
│  │  │  │- Context    │ │- Goal Decomp│ │- Logic Flow │   │ │ │
│  │  │  │- History    │ │- Sub-agents │ │- Routing    │   │ │ │
│  │  │  │- Learning   │ │- Scheduling │ │- Fallbacks  │   │ │ │
│  │  │  └─────────────┘ └─────────────┘ └─────────────┘   │ │ │
│  │  └─────────────────────────────────────────────────────┘ │ │
│  │                              │                           │ │
│  │                              ▼                           │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │              Vertex AI Integration                  │ │ │
│  │  │  - Gemini Pro for Natural Language Processing      │ │ │
│  │  │  - PaLM 2 for Complex Reasoning                    │ │ │
│  │  │  - Vector Embeddings for Semantic Search           │ │ │
│  │  │  - ML Model Training & Inference                   │ │ │
│  │  └─────────────────────────────────────────────────────┘ │ │
│  └─────────────────────┬───────────────┬───────────────────┘ │
│                       │               │                     │
│  ┌────────────────────▼───────────────▼─────────────────────┐ │
│  │                    SUB-AGENTS                           │ │
│  │  ┌─────────────────────────┐  ┌─────────────────────────┐ │ │
│  │  │  SERVICE MATCHING AGENT │  │ COMMUNITY INTELLIGENCE │ │ │
│  │  │                         │  │        AGENT            │ │ │
│  │  │  Core Responsibilities: │  │                         │ │ │
│  │  │  ┌─────────────────────┐ │  │  Core Responsibilities: │ │ │
│  │  │  │• Provider Discovery │ │  │  ┌─────────────────────┐ │ │ │
│  │  │  │• Intelligent Ranking│ │  │  │• Local Event Analysis│ │ │ │
│  │  │  │• Trust Assessment   │ │  │  │• Community Insights │ │ │ │
│  │  │  │• Semantic Matching  │ │  │  │• Notification Logic │ │ │ │
│  │  │  │• Learning from      │ │  │  │• Trend Detection    │ │ │ │
│  │  │  │  User Interactions  │ │  │  │• Content Curation  │ │ │ │
│  │  │  │• Neo4j Graph Query  │ │  │  │• Engagement Opt.   │ │ │ │
│  │  │  └─────────────────────┘ │  │  └─────────────────────┘ │ │ │
│  │  │                         │  │                         │ │ │
│  │  │  AI Capabilities:       │  │  AI Capabilities:       │ │ │
│  │  │  • Vector Embeddings   │  │  • NLP Processing       │ │ │
│  │  │  • Graph Neural Networks│  │  • Sentiment Analysis   │ │ │
│  │  │  • Collaborative Filter │  │  • Time Series Forecast │ │ │
│  │  │  • Reinforcement Learn  │  │  • Social Network Anal. │ │ │
│  │  └─────────────────────────┘  └─────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**AI Features Solving Business Problems:**
- **Smart Discovery**: Intelligent ranking reduces time to find quality providers
- **Trust Building**: Verification-weighted results build confidence
- **Proactive Help**: Nudges guide providers to improve their visibility
- **Local Intelligence**: Community-aware suggestions enhance relevance

### 3. MULTI-DATABASE ARCHITECTURE

#### A. Neo4j Knowledge Graph (Ontology Database)
```
┌─────────────────────────────────────────────────────────────┐
│                    NEO4J KNOWLEDGE GRAPH                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    NODE TYPES                           │ │
│  │                                                         │ │
│  │  (Consumer)  ─LIVES_IN─>  (Location)                   │ │
│  │      │                       │                         │ │
│  │      │                       │                         │ │
│  │  ─SEEKS─>   (Service)    <─SERVES─  (Provider)        │ │
│  │      │          │                       │               │ │
│  │      │          │                       │               │ │
│  │  ─TRUSTS─>  (Review) <─PROVIDES─   ─VERIFIED_BY─>     │ │
│  │                                        │               │ │
│  │                                    (Admin)             │ │
│  │                                                         │ │
│  │  Relationship Types:                                    │ │
│  │  • LIVES_IN (Consumer -> Location)                     │ │
│  │  • SERVES (Provider -> Location)                       │ │
│  │  • OFFERS (Provider -> Service)                        │ │
│  │  • SEEKS (Consumer -> Service)                         │ │
│  │  • INQUIRED_ABOUT (Consumer -> Provider)               │ │
│  │  • SIMILAR_TO (Service -> Service)                     │ │
│  │  • COMPETES_WITH (Provider -> Provider)                │ │
│  │  • BELONGS_TO (Location -> District)                   │ │
│  │  • SPECIALIZES_IN (Provider -> ServiceCategory)        │ │
│  │  • RECOMMENDS (AI_Agent -> Provider)                   │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                GRAPH ALGORITHMS                         │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │Path Finding │ │Community    │ │Similarity   │      │ │
│  │  │- Shortest   │ │Detection    │ │Algorithms   │      │ │
│  │  │- Weighted   │ │- Clustering │ │- Collaborative│    │ │
│  │  │- Multi-hop  │ │- Influence  │ │- Content-based│    │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### B. PostgreSQL (Relational Data)
```
┌─────────────────────────────────────────────────────────────┐
│                     POSTGRESQL SCHEMA                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    CORE TABLES                          │ │
│  │                                                         │ │
│  │  users                    providers                     │ │
│  │  ├── id (UUID)            ├── id (UUID)                │ │
│  │  ├── email               ├── user_id (FK)              │ │
│  │  ├── password_hash       ├── business_name             │ │
│  │  ├── user_type           ├── description               │ │
│  │  ├── created_at          ├── contact_info              │ │
│  │  └── updated_at          ├── verification_status       │ │
│  │                          ├── service_categories        │ │
│  │  inquiries               └── location_data             │ │
│  │  ├── id (UUID)                                         │ │
│  │  ├── consumer_id (FK)     community_posts              │ │
│  │  ├── provider_id (FK)     ├── id (UUID)                │ │
│  │  ├── message              ├── title                     │ │
│  │  ├── status               ├── content                   │ │
│  │  ├── created_at           ├── author_id (FK)            │ │
│  │  └── responded_at         ├── target_locations          │ │
│  │                          ├── post_type                 │ │
│  │  analytics_events        ├── status                    │ │
│  │  ├── id (UUID)            ├── created_at                │ │
│  │  ├── user_id (FK)         └── expires_at               │ │
│  │  ├── event_type                                        │ │
│  │  ├── properties (JSONB)                                │ │
│  │  └── timestamp                                         │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### C. Firebase (Real-time & Authentication)
```
┌─────────────────────────────────────────────────────────────┐
│                    FIREBASE SERVICES                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                AUTHENTICATION                           │ │
│  │  • Identity Management                                  │ │
│  │  • JWT Token Generation                                 │ │
│  │  • Multi-factor Authentication                          │ │
│  │  • Social Login Integration                             │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              REAL-TIME DATABASE                         │ │
│  │  • Live Chat Messages                                   │ │
│  │  • Notification Queues                                  │ │
│  │  • Real-time Status Updates                             │ │
│  │  • Live Location Tracking                               │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                FILE STORAGE                             │ │
│  │  • Profile Images                                       │ │
│  │  • Service Portfolio Images                             │ │
│  │  • Document Uploads                                     │ │
│  │  • AI Model Files                                       │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### D. Redis (Caching & Sessions)
```
┌─────────────────────────────────────────────────────────────┐
│                     REDIS CACHE LAYER                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                 CACHE STRATEGIES                        │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │Session Cache│ │Query Cache  │ │ML Cache     │      │ │
│  │  │- User tokens│ │- DB Results │ │- Embeddings │      │ │
│  │  │- Auth state │ │- Search     │ │- Predictions│      │ │
│  │  │- Preferences│ │- Aggregates │ │- Model Res. │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                  REAL-TIME DATA                         │ │
│  │  • Live User Locations                                  │ │
│  │  • Active Sessions                                      │ │
│  │  • Rate Limiting Counters                               │ │
│  │  • Notification Queues                                  │ │
│  │  • AI Agent States                                      │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 4. SECURITY & COMPLIANCE ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                  SECURITY & COMPLIANCE LAYER                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    PDPA COMPLIANCE                      │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │Consent Mgmt │ │Data Min.    │ │User Rights  │      │ │
│  │  │- Explicit   │ │- Purpose    │ │- Access     │      │ │
│  │  │- Granular   │ │- Necessary  │ │- Correction │      │ │
│  │  │- Withdraw   │ │- Retention  │ │- Deletion   │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                 FIREBASE SECURITY                       │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │Auth Rules   │ │Firestore    │ │Storage      │      │ │
│  │  │- Role-based │ │Rules        │ │Security     │      │ │
│  │  │- JWT Tokens │ │- Read/Write │ │- File Types │      │ │
│  │  │- Session    │ │- Validation │ │- Size Limits│      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5. DEPLOYMENT ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT ARCHITECTURE                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                   MOBILE DEPLOYMENT                     │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │Development  │ │Testing      │ │Production   │      │ │
│  │  │- Expo Go    │ │- EAS Build  │ │- Play Store │      │ │
│  │  │- Hot Reload │ │- TestFlight │ │- App Store  │      │ │
│  │  │- Debug      │ │- Beta       │ │- OTA Updates│      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    WEB DEPLOYMENT                       │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │Admin Panel  │ │Privacy      │ │Analytics    │      │ │
│  │  │- Firebase   │ │Policy       │ │- Dashboard  │      │ │
│  │  │- Hosting    │ │- Legal Docs │ │- Reporting  │      │ │
│  │  │- CI/CD      │ │- Terms      │ │- Monitoring │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Problem-Solution Mapping

### Business Problems → Architecture Solutions

1. **Discovery Problem**: "Hard to find trusted local services"
   - **Solution**: Smart matching algorithm + verification system + location-based filtering
   - **Components**: Agentic AI Engine + Firestore geo-queries + Provider verification workflow

2. **Trust Problem**: "Difficult to assess service provider reliability"
   - **Solution**: Manual verification + profile completeness scoring + community feedback
   - **Components**: Admin verification system + Agentic profile scoring + User review system

3. **Fragmented Information**: "Local announcements scattered across platforms"
   - **Solution**: Centralized community feed + admin-managed content + push notifications
   - **Components**: Community collection + Admin panel + FCM notifications

4. **Provider Visibility**: "Local businesses struggle to reach customers"
   - **Solution**: Easy profile creation + intelligent ranking + inquiry management
   - **Components**: Provider app + Top Picks algorithm + Inquiry system

5. **Time & Effort**: "Manual searching is inefficient"
   - **Solution**: Category-based browsing + one-tap actions + proactive suggestions
   - **Components**: React Native UI + Firebase real-time + Agentic recommendations

## Technology Stack Justification

### Why React Native + Expo Go?
- **Single Codebase**: Develop once, deploy to both Android and iOS
- **Rapid Prototyping**: Expo Go enables instant testing on devices without complex setup
- **Solo Developer Friendly**: Managed workflow reduces native development complexity
- **Sri Lankan Market**: Cost-effective for local market entry
- **Hot Reload**: Fast development iteration cycles

### Why Python FastAPI + Unicorn?
- **High Performance**: Async support with Unicorn ASGI server
- **AI/ML Integration**: Native Python ecosystem for LangChain, Vertex AI
- **Auto Documentation**: OpenAPI/Swagger documentation generation
- **Type Safety**: Pydantic models for data validation
- **Rapid Development**: Fast API development with minimal boilerplate

### Why Node.js/Express.js?
- **Real-time Features**: Excellent WebSocket and Socket.io support
- **JavaScript Ecosystem**: Large npm package ecosystem
- **Microservices**: Lightweight for specific real-time services
- **Firebase Integration**: Native SDK support

### Why SpringBoot (Java)?
- **Enterprise Security**: Robust security framework for sensitive operations
- **Batch Processing**: Excellent for data processing and analytics
- **Scalability**: Proven enterprise-grade scalability
- **Integration**: Strong database and message queue integrations

### Why Neo4j (Knowledge Graph)?
- **Relationship Modeling**: Perfect for service provider connections and recommendations
- **Graph Algorithms**: Built-in algorithms for community detection and pathfinding  
- **Semantic Queries**: Complex relationship-based queries for AI agents
- **Ontology Support**: Knowledge representation for domain expertise
- **Real-time Graph Analytics**: Live relationship analysis for recommendations

### Why PostgreSQL?
- **ACID Compliance**: Reliable transactions for critical business data
- **Complex Queries**: Advanced SQL capabilities for analytics
- **JSONB Support**: Flexible schema for evolving data structures
- **Performance**: Excellent performance with proper indexing
- **Ecosystem**: Mature tooling and monitoring solutions

### Why LangChain + Vertex AI?
- **Agent Framework**: LangChain provides orchestration for multi-agent systems
- **Google Integration**: Vertex AI offers Gemini Pro and PaLM 2 models
- **Memory Management**: LangChain handles agent memory and context
- **Tool Integration**: Easy integration with external APIs and databases
- **Prompt Engineering**: Advanced prompt management and optimization

### Why Redis?
- **High Performance**: In-memory operations for sub-millisecond response times
- **Session Management**: Distributed session storage across multiple servers
- **Caching**: Intelligent caching for database queries and ML predictions
- **Real-time Data**: Pub/Sub for real-time notifications
- **Rate Limiting**: Built-in rate limiting and throttling capabilities

### Why Firebase (Limited Use)?
- **Authentication**: Battle-tested identity management
- **Real-time Database**: Live updates for chat and notifications
- **File Storage**: Managed file storage with CDN
- **Push Notifications**: Firebase Cloud Messaging integration

## Agentic AI System Design

### Orchestration Agent Responsibilities
1. **Task Coordination**: Manages communication between sub-agents
2. **Decision Making**: High-level business logic and routing decisions
3. **Context Management**: Maintains conversation state and user context
4. **Error Handling**: Graceful fallback strategies when sub-agents fail
5. **Learning Integration**: Incorporates feedback to improve agent performance

### Service Matching Agent
**Primary Goal**: Intelligently match consumers with optimal service providers

**Key Capabilities**:
- **Semantic Understanding**: Uses Vertex AI embeddings to understand service requests beyond keywords
- **Graph Traversal**: Leverages Neo4j to find optimal provider-consumer connections
- **Learning System**: Continuously improves matching based on successful connections
- **Trust Scoring**: Evaluates provider reliability using multiple signals
- **Location Intelligence**: Sophisticated geographic and proximity-based matching

**Business Problem Solved**: Eliminates the time-consuming process of manually searching through service providers

### Community Intelligence Agent  
**Primary Goal**: Provide proactive, relevant local information and optimize community engagement

**Key Capabilities**:
- **Event Processing**: Analyzes local events and their relevance to users
- **Trend Detection**: Identifies emerging community needs and opportunities
- **Notification Optimization**: Determines optimal timing and content for notifications
- **Content Curation**: Automatically categorizes and prioritizes community content
- **Engagement Analytics**: Measures and optimizes community participation

**Business Problem Solved**: Addresses information fragmentation by providing centralized, intelligently curated local information

## Agent Interaction Patterns

### Consumer Request Flow
```
Consumer Query → Orchestration Agent → Service Matching Agent → Neo4j Graph Traversal → 
Ranked Results → Orchestration Agent → Consumer Response
```

### Community Update Flow  
```
Local Event Data → Community Intelligence Agent → Relevance Analysis → 
User Segmentation → Orchestration Agent → Targeted Notifications
```

### Cross-Agent Learning
```
User Feedback → Orchestration Agent → Updates Both Sub-Agents → 
Improved Future Performance
```

This architecture directly addresses all identified business problems while being feasible for a solo developer within your 3-month MVP timeline.