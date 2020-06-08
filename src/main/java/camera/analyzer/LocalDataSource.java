package camera.analyzer;

import java.time.LocalDateTime;
import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.TimeZone;

public class LocalDataSource implements DataSource {
    private final List<EventObserver> observers = new ArrayList<>();

    public LocalDataSource() {
        new Thread(() -> {
            LocalDateTime lastScannedAt = dateTimeNow();
            Repository repository = Repository.getInstance();
            while (true) {
                try {
                    Thread.sleep(500);
                    List<Event> events = repository.getEventsAfterOrEqual(lastScannedAt);
                    lastScannedAt = dateTimeNow();
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

    private LocalDateTime dateTimeNow() {
        TimeZone timeZoneServer = TimeZone.getDefault();
        ZonedDateTime zonedDate = LocalDateTime.now().atZone(timeZoneServer.toZoneId());

        TimeZone timeZoneUTC = TimeZone.getTimeZone("UTC");
        ZonedDateTime zonedDateUTC = zonedDate.withZoneSameInstant(timeZoneUTC.toZoneId());
        LocalDateTime dateTimeUTC = zonedDateUTC.toLocalDateTime();

        return dateTimeUTC;
    }
}
