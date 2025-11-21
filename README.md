# KumbuK - Hyper-Local Community Services Hub# Kumbuk - Hyper-Local Community Services Hub



AI-powered platform connecting consumers with local service providers in Sri Lanka.A React Native monorepo built with Nx for managing consumer and service provider mobile applications.



## 🚀 Project Structure## 🏗️ Project Structure



``````

Kumbuk_Hyper-Local-Community-Services-Hub-/Kumbuk_Hyper-Local-Community-Services-Hub-/

├── frontend/          # React Native mobile apps (Nx monorepo)├── apps/

│   ├── apps/          # consumer-app, provider-app│   ├── consumer-app/          # Consumer mobile app (React Native + Expo)

│   └── libs/          # Shared libraries│   └── provider-app/          # Service provider mobile app (React Native + Expo)

├── backend/           # Python FastAPI backend with AI agents├── libs/

│   ├── app/           # Application code│   ├── ui-shared/             # Shared UI components and themes

│   └── venv/          # Virtual environment│   ├── models/                # Shared TypeScript types and interfaces

├── docs/              # Project documentation│   └── utils/                 # Shared utility functions

└── scripts/           # Utility scripts└── tools/                     # Development tools and scripts

``````



## 📋 Prerequisites## 🚀 Getting Started



- **Python 3.9+** (for backend)### Prerequisites

- **Node.js 16+** (for frontend)

- **npm or yarn** (package manager)- Node.js (v18 or higher)

- **Expo Go app** (on your mobile device)- npm or yarn

- Expo CLI (`npm install -g @expo/cli`)

## 🎯 Quick Start- Expo Go app on your mobile device



### Backend (Terminal 1)### Installation



```powershell1. **Install dependencies**:

cd backend

python -m venv venv```bash

.\venv\Scripts\Activate.ps1npm install --legacy-peer-deps

pip install -r requirements.txt```

python -m uvicorn app.main:app --reload

```2. **Start the consumer app**:



**Backend runs at**: http://localhost:8000```bash

npx nx start consumer-app

### Frontend (Terminal 2)```



```powershell3. **Start the provider app**:

cd frontend

npm install```bash

npx nx start consumer-appnpx nx start provider-app

``````



**Then**: Scan QR code with Expo Go to open on mobile device### 📱 Mobile Development



## 📚 Documentation#### Running on Device with Expo Go



- [**Integration Guide**](docs/README_INTEGRATION.md) - Complete setup & usage1. Install Expo Go on your mobile device

- [**Architecture Diagrams**](docs/ARCHITECTURE_DIAGRAMS.md) - System architecture2. Start the development server: `npx nx start consumer-app`

- [**Quick Reference**](docs/QUICK_REFERENCE.md) - Common commands & tips3. Scan the QR code with Expo Go (Android) or Camera app (iOS)

- [**AI Agent Architecture**](docs/AI_Agent_Architecture_Guide.md) - Agent design

#### Available Commands

## 🛠️ Technology Stack

```bash

### Frontend# Development

- React Native + Exponpx nx start consumer-app                    # Start consumer app

- TypeScriptnpx nx start provider-app                    # Start provider app

- Nx monorepo

- WebSocket# Testing

npx nx test consumer-app                     # Test consumer app

### Backendnpx nx test provider-app                     # Test provider app

- Python + FastAPInpx nx test ui-shared                        # Test shared UI components

- Pydantic

- AI Agents (Consumer, Provider)# Linting

- Orchestration Layernpx nx lint consumer-app                     # Lint consumer app

npx nx lint provider-app                     # Lint provider app

### Cloud (Planned)```

- Google Cloud Platform

- Firebase## 📚 Shared Libraries

- Vertex AI (Gemini-Pro)

- Neo4j Aura### @kumbuk/ui-shared



## 🎨 FeaturesContains shared UI components, themes, colors, and styling constants.



✅ Multi-agent AI system  ```typescript

✅ Real-time chat interface  import { colors, theme, typography } from '@kumbuk/ui-shared';

✅ WebSocket + HTTP APIs  ```

✅ Service search & recommendations  

✅ Provider business analytics  ### @kumbuk/models



## 📱 Mobile AppsContains TypeScript interfaces and types for domain models.



- **Consumer App**: Find local service providers, chat with AI assistant```typescript

- **Provider App**: Manage business, view analytics, handle inquiriesimport { User, ServiceProvider, Inquiry } from '@kumbuk/models';

```

## 🔌 API Endpoints

### @kumbuk/utils

- Backend API: http://localhost:8000

- API Documentation: http://localhost:8000/docsContains utility functions for formatting, validation, and common operations.

- Health Check: http://localhost:8000/health

```typescript

## 📄 Licenseimport { formatPhoneNumber, validateEmail } from '@kumbuk/utils';

```

Educational Project - Cloud Computing Course

## 🛠️ Development Workflow

---

### Using Shared Libraries

**Last Updated**: October 2025

```typescript
// In any app component
import { User, ServiceProvider } from '@kumbuk/models';
import { colors, spacing } from '@kumbuk/ui-shared';
import { formatPhoneNumber } from '@kumbuk/utils';

const MyComponent = () => {
  const formattedPhone = formatPhoneNumber('0771234567');

  return (
    <View style={{ padding: spacing.md, backgroundColor: colors.background }}>
      {/* Your component JSX */}
    </View>
  );
};
```

## 📱 App Features

### Consumer App

- Service provider discovery
- Category-based browsing
- Location-based filtering
- One-tap communication
- Community feed

### Provider App

- Business profile management
- Service listing
- Inquiry management
- Analytics tracking
- Verification management

---

**Quick Start:** Run `npx nx start consumer-app` to begin development!
