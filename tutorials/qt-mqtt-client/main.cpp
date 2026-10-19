#include <QApplication>
#include <QElapsedTimer>
#include <QGridLayout>
#include <QLabel>
#include <QMap>
#include <QPushButton>
#include <QRandomGenerator>
#include <QSslConfiguration>
#include <QTimer>
#include <QWidget>
#include <QtMqtt/QMqttClient>
#include <QtMqtt/QMqttSubscription>

class PressPanel : public QWidget {
public:
    explicit PressPanel(QWidget *parent = nullptr) : QWidget(parent) {
        m_prefix = qEnvironmentVariable("MQTT_TOPIC_PREFIX",
                                        "connectmq/demo/qt-hmi-3f81") + "/line1/press1";
        buildUi();
        setupClient();

        m_staleTimer.setInterval(1000);
        connect(&m_staleTimer, &QTimer::timeout, this, &PressPanel::checkStale);
        m_staleTimer.start();

        m_reconnectTimer.setSingleShot(true);
        connect(&m_reconnectTimer, &QTimer::timeout, this, &PressPanel::connectToBroker);

        connectToBroker();
    }

private:
    struct Tag { QLabel *value; QElapsedTimer age; QString unit; };

    void buildUi() {
        auto *grid = new QGridLayout(this);
        QFont big = font();
        big.setPointSize(28);
        big.setBold(true);

        const QList<QPair<QString, QString>> tags = {
            {"temperature", " °C"}, {"pressure", " bar"}, {"state", ""}};
        int row = 0;
        for (const auto &[name, unit] : tags) {
            auto *caption = new QLabel(name.toUpper(), this);
            auto *value = new QLabel("--", this);
            value->setFont(big);
            grid->addWidget(caption, row, 0);
            grid->addWidget(value, row, 1);
            m_tags.insert(name, Tag{value, QElapsedTimer(), unit});
            ++row;
        }

        m_startBtn = new QPushButton("START", this);
        m_stopBtn = new QPushButton("STOP", this);
        grid->addWidget(m_startBtn, row, 0);
        grid->addWidget(m_stopBtn, row, 1);
        connect(m_startBtn, &QPushButton::clicked, this, [this] { sendCommand("START"); });
        connect(m_stopBtn, &QPushButton::clicked, this, [this] { sendCommand("STOP"); });

        m_status = new QLabel(this);
        grid->addWidget(m_status, row + 1, 0, 1, 2);
        setCommandsEnabled(false);
    }

    void setupClient() {
        const QString clientId = qEnvironmentVariable(
            "MQTT_CLIENT_ID",
            QString("qt-hmi-%1").arg(QRandomGenerator::global()->generate(), 8, 16, QChar('0')));

        m_client.setHostname("broker.connectmq.com");
        m_client.setPort(8883);
        m_client.setClientId(clientId);
        m_client.setUsername(qEnvironmentVariable("MQTT_USERNAME"));
        m_client.setPassword(qEnvironmentVariable("MQTT_PASSWORD"));
        m_client.setProtocolVersion(QMqttClient::MQTT_5_0);
        m_client.setKeepAlive(30);
        m_client.setCleanSession(true);

        connect(&m_client, &QMqttClient::connected, this, [this] {
            m_backoffMs = 1000;
            m_status->setText("Connected to " + m_client.hostname());
            setCommandsEnabled(true);
            auto *sub = m_client.subscribe(QMqttTopicFilter(m_prefix + "/+"), 1);
            if (!sub) {
                m_status->setText("Subscribe failed");
                return;
            }
            // UniqueConnection: Qt may hand back the same subscription object
            // after a reconnect, and we must not handle each message twice.
            connect(sub, &QMqttSubscription::messageReceived, this,
                    &PressPanel::onMessage, Qt::UniqueConnection);
        });

        connect(&m_client, &QMqttClient::disconnected, this, [this] {
            setCommandsEnabled(false);
            m_status->setText(QString("Disconnected (error %1), retrying in %2 s")
                                  .arg(int(m_client.error()))
                                  .arg(m_backoffMs / 1000));
            m_reconnectTimer.start(m_backoffMs);
            m_backoffMs = qMin(m_backoffMs * 2, 30000);
        });
    }

    void connectToBroker() {
        m_status->setText("Connecting...");
        m_client.connectToHostEncrypted(QSslConfiguration::defaultConfiguration());
    }

    void onMessage(const QMqttMessage &msg) {
        const QString name = msg.topic().levels().last();
        auto it = m_tags.find(name);
        if (it == m_tags.end())
            return;
        const QString text = QString::fromUtf8(msg.payload()).trimmed();
        if (name != "state") {
            bool ok = false;
            const double v = text.toDouble(&ok);
            if (!ok) return;                         // ignore malformed payloads
            it->value->setText(QString::number(v, 'f', 1) + it->unit);
        } else {
            it->value->setText(text.left(16));
            it->value->setStyleSheet(text == "FAULT" ? "color: #c62828;" : "");
        }
        it->age.restart();
        if (name != "state") it->value->setStyleSheet("");
    }

    void checkStale() {
        for (auto &tag : m_tags) {
            if (tag.age.isValid() && tag.age.elapsed() > 10000)
                tag.value->setStyleSheet("color: #9e9e9e;");   // grey = stale
        }
    }

    void sendCommand(const QString &cmd) {
        const qint32 id = m_client.publish(QMqttTopicName(m_prefix + "/cmd"), cmd.toUtf8(), 1, false);
        if (id == -1)
            m_status->setText("Publish failed");
    }

    void setCommandsEnabled(bool on) {
        m_startBtn->setEnabled(on);
        m_stopBtn->setEnabled(on);
    }

    QMqttClient m_client;
    QMap<QString, Tag> m_tags;
    QString m_prefix;
    QLabel *m_status = nullptr;
    QPushButton *m_startBtn = nullptr;
    QPushButton *m_stopBtn = nullptr;
    QTimer m_staleTimer;
    QTimer m_reconnectTimer;
    int m_backoffMs = 1000;
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    PressPanel panel;
    panel.setWindowTitle("Press 1 HMI");
    panel.resize(420, 300);
    panel.show();
    return app.exec();
}
