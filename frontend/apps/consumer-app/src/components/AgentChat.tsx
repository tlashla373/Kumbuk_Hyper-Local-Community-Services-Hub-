import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
} from 'react-native';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'agent';
  timestamp: Date;
  type?: string;
  data?: any;
}

interface AgentChatProps {
  userId: string;
  apiUrl?: string;
}

export const AgentChat: React.FC<AgentChatProps> = ({
  userId,
  apiUrl = 'http://localhost:8000',
}) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "Hello! I'm your KumbuK assistant. How can I help you today?",
      sender: 'agent',
      timestamp: new Date(),
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>('');
  const [ws, setWs] = useState<WebSocket | null>(null);
  const flatListRef = useRef<FlatList>(null);

  // Initialize WebSocket connection
  useEffect(() => {
    const websocket = new WebSocket(`ws://localhost:8000/ws/${userId}`);

    websocket.onopen = () => {
      console.log('WebSocket Connected');
    };

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      handleAgentResponse(data);
    };

    websocket.onerror = (error) => {
      console.error('WebSocket Error:', error);
    };

    websocket.onclose = () => {
      console.log('WebSocket Disconnected');
    };

    setWs(websocket);

    return () => {
      websocket.close();
    };
  }, [userId]);

  // Generate session ID on mount
  useEffect(() => {
    const newSessionId = `session_${userId}_${Date.now()}`;
    setSessionId(newSessionId);
  }, [userId]);

  const handleAgentResponse = (data: any) => {
    setIsLoading(false);

    const agentMessage: Message = {
      id: Date.now().toString(),
      text: data.response || data.message || 'I received your message.',
      sender: 'agent',
      timestamp: new Date(),
      type: data.type,
      data: data,
    };

    setMessages((prev) => [...prev, agentMessage]);
  };

  const sendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      // Try WebSocket first
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(
          JSON.stringify({
            message: userMessage.text,
            session_id: sessionId,
          })
        );
      } else {
        // Fallback to HTTP
        const response = await fetch(`${apiUrl}/message`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: userMessage.text,
            user_id: userId,
            session_id: sessionId,
          }),
        });

        const data = await response.json();
        handleAgentResponse(data);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setIsLoading(false);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          text: 'Sorry, I could not connect to the server. Please try again.',
          sender: 'agent',
          timestamp: new Date(),
        },
      ]);
    }
  };

  const renderMessage = ({ item }: { item: Message }) => {
    const isUser = item.sender === 'user';

    return (
      <View
        style={[
          styles.messageContainer,
          isUser ? styles.userMessage : styles.agentMessage,
        ]}
      >
        <Text
          style={[
            styles.messageText,
            isUser ? styles.userMessageText : styles.agentMessageText,
          ]}
        >
          {item.text}
        </Text>
        <Text style={styles.timestamp}>
          {item.timestamp.toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </Text>

        {/* Render suggestions if available */}
        {item.data?.suggestions && (
          <View style={styles.suggestionsContainer}>
            {item.data.suggestions.map((suggestion: string, index: number) => (
              <TouchableOpacity
                key={index}
                style={styles.suggestionButton}
                onPress={() => {
                  setInputText(suggestion);
                }}
              >
                <Text style={styles.suggestionText}>{suggestion}</Text>
              </TouchableOpacity>
            ))}
          </View>
        )}

        {/* Render provider list if available */}
        {item.data?.providers && (
          <View style={styles.providersContainer}>
            {item.data.providers.map((provider: any) => (
              <View key={provider.id} style={styles.providerCard}>
                <Text style={styles.providerName}>{provider.name}</Text>
                <Text style={styles.providerDetails}>
                  ⭐ {provider.rating} • {provider.location}
                </Text>
                <Text style={styles.providerPrice}>{provider.price_range}</Text>
              </View>
            ))}
          </View>
        )}
      </View>
    );
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={90}
    >
      <View style={styles.header}>
        <Text style={styles.headerTitle}>KumbuK Assistant</Text>
        <View
          style={[
            styles.statusIndicator,
            ws?.readyState === WebSocket.OPEN
              ? styles.statusConnected
              : styles.statusDisconnected,
          ]}
        />
      </View>

      <FlatList
        ref={flatListRef}
        data={messages}
        renderItem={renderMessage}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.messagesList}
        onContentSizeChange={() => flatListRef.current?.scrollToEnd()}
      />

      {isLoading && (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="small" color="#007AFF" />
          <Text style={styles.loadingText}>Agent is typing...</Text>
        </View>
      )}

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={inputText}
          onChangeText={setInputText}
          placeholder="Type your message..."
          multiline
          maxLength={500}
          editable={!isLoading}
        />
        <TouchableOpacity
          style={[
            styles.sendButton,
            (!inputText.trim() || isLoading) && styles.sendButtonDisabled,
          ]}
          onPress={sendMessage}
          disabled={!inputText.trim() || isLoading}
        >
          <Text style={styles.sendButtonText}>Send</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  statusIndicator: {
    width: 12,
    height: 12,
    borderRadius: 6,
  },
  statusConnected: {
    backgroundColor: '#4CAF50',
  },
  statusDisconnected: {
    backgroundColor: '#F44336',
  },
  messagesList: {
    padding: 16,
    paddingBottom: 8,
  },
  messageContainer: {
    maxWidth: '80%',
    marginBottom: 12,
    padding: 12,
    borderRadius: 16,
  },
  userMessage: {
    alignSelf: 'flex-end',
    backgroundColor: '#007AFF',
  },
  agentMessage: {
    alignSelf: 'flex-start',
    backgroundColor: '#FFFFFF',
    borderWidth: 1,
    borderColor: '#E0E0E0',
  },
  messageText: {
    fontSize: 16,
    lineHeight: 22,
  },
  userMessageText: {
    color: '#FFFFFF',
  },
  agentMessageText: {
    color: '#333',
  },
  timestamp: {
    fontSize: 11,
    color: '#999',
    marginTop: 4,
  },
  suggestionsContainer: {
    marginTop: 12,
  },
  suggestionButton: {
    backgroundColor: '#F0F0F0',
    padding: 8,
    borderRadius: 8,
    marginTop: 6,
  },
  suggestionText: {
    color: '#007AFF',
    fontSize: 14,
  },
  providersContainer: {
    marginTop: 12,
  },
  providerCard: {
    backgroundColor: '#F9F9F9',
    padding: 12,
    borderRadius: 8,
    marginTop: 8,
    borderLeftWidth: 3,
    borderLeftColor: '#007AFF',
  },
  providerName: {
    fontSize: 15,
    fontWeight: '600',
    color: '#333',
  },
  providerDetails: {
    fontSize: 13,
    color: '#666',
    marginTop: 4,
  },
  providerPrice: {
    fontSize: 13,
    color: '#007AFF',
    marginTop: 4,
  },
  loadingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
    backgroundColor: '#F9F9F9',
  },
  loadingText: {
    marginLeft: 8,
    color: '#666',
    fontSize: 14,
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 12,
    backgroundColor: '#FFFFFF',
    borderTopWidth: 1,
    borderTopColor: '#E0E0E0',
  },
  input: {
    flex: 1,
    backgroundColor: '#F5F5F5',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 10,
    marginRight: 8,
    maxHeight: 100,
    fontSize: 16,
  },
  sendButton: {
    backgroundColor: '#007AFF',
    borderRadius: 20,
    paddingHorizontal: 20,
    paddingVertical: 10,
    justifyContent: 'center',
  },
  sendButtonDisabled: {
    backgroundColor: '#CCCCCC',
  },
  sendButtonText: {
    color: '#FFFFFF',
    fontWeight: '600',
    fontSize: 16,
  },
});
