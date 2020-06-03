package camera.analyzer;

import java.time.LocalDateTime;

public class Event {
    private final String name;
    private final LocalDateTime occurredAt;
    private final double confidence;

    public Event(String name, LocalDateTime occurredAt, double confidence) {
        this.name = name;
        this.occurredAt = occurredAt;
        this.confidence = confidence;
    }

    public String getName() {
        return name;
    }

    public LocalDateTime getOccurredAt() {
        return occurredAt;
    }

    public double getConfidence() {
        return confidence;
    }
}
