package camera.analyzer;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

public class LocalDataSource implements DataSource {
    private final List<EventObserver> observers = new ArrayList<>();

    public LocalDataSource() {
        new Thread(() -> {
            LocalDateTime lastScannedAt = LocalDateTime.now();
            Repository repository = Repository.getInstance();
            while (true) {
                try {
                    Thread.sleep(500);
                    List<Event> events = repository.getEventsAfterOrEqual(lastScannedAt);
                    lastScannedAt = LocalDateTime.now();
                    events.forEach(e -> observers.forEach(observer -> observer.onNext(e)));
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }

    @Override
    public void registerObserver(EventObserver observer) {
        observers.add(observer);
    }

}
