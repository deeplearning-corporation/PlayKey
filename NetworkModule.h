// NetworkModule.h
#pragma once

#ifdef NETWORKMODULE_EXPORTS
#define NETWORKMODULE_API __declspec(dllexport)
#else
#define NETWORKMODULE_API __declspec(dllimport)
#endif

#include <string>
#include <functional>

// 回调函数类型
typedef std::function<void(int, const char*)> MessageCallback;

class NETWORKMODULE_API NetworkModule {
public:
    NetworkModule();
    ~NetworkModule();

    // 连接管理
    bool Connect(const char* serverAddress, int port);
    void Disconnect();
    bool IsConnected();

    // 数据传输
    bool SendData(const char* data, int length);
    void SetMessageCallback(MessageCallback callback);

    // 房间管理
    bool CreateRoom(const char* roomName, int maxPlayers);
    bool JoinRoom(const char* roomName);
    void LeaveRoom();

    // 玩家数据
    void UpdatePlayerData(const char* playerData);
    void RequestPlayerList();

    // 排行榜
    void RequestLeaderboard();
    void SubmitScore(const char* playerName, int score);

private:
    void* m_socket;
    bool m_connected;
    std::string m_currentRoom;
    MessageCallback m_messageCallback;
};