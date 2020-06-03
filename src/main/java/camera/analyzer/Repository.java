package camera.analyzer;

import java.sql.Connection;
import java.sql.Date;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.time.format.ResolverStyle;
import java.time.temporal.TemporalAccessor;
import java.util.ArrayList;
import java.util.List;

public class Repository {
    private static Repository INSTANCE = null;

    private static final String JDBC_URL = "jdbc:sqlite:data.db";
    private static final String DRIVER = "org.sqlite.JDBC";

    private Connection connection;

    private Repository() {
        try {
            Class.forName(Repository.DRIVER);
        } catch (ClassNotFoundException e) {
            System.err.println("add SQLite driver to libs");
            throw new RuntimeException(e);
        }

        try {
            connection = DriverManager.getConnection(JDBC_URL);
            connection.createStatement();
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }

    public static Repository getInstance() {
        synchronized (Repository.class) {
            if (INSTANCE == null) {
                INSTANCE = new Repository();
            }
            return INSTANCE;
        }
    }

    DateTimeFormatter sqlDateFormat = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    public List<Event> getEventsAfterOrEqual(LocalDateTime lastScannedAt) throws SQLException {
        List<Event> results = new ArrayList<>();
        PreparedStatement preparedStatement = connection.prepareStatement("SELECT * FROM events where date >= ?;");
        preparedStatement.setString(1, sqlDateFormat.format(lastScannedAt));
        ResultSet result = preparedStatement.executeQuery();
        while (result.next()) {
            String name = result.getString("object");
            String confidenceString = result.getString("confidence");
            double confidence = Double.parseDouble(confidenceString);
            String date = result.getString("date");
            //todo parse date
//            LocalDateTime localDateTime = LocalDateTime.parse(date,sqlDateFormat);
            results.add(new Event(name, LocalDateTime.now(), confidence));
        }
        return results;
    }
}