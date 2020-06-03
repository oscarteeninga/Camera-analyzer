package camera.analyzer;

public class Repository {
    private static Repository INSTANCE = null;

    private static final String JDBC_URL = "jdbc:sqlite:requests.db";
    private static final String DRIVER = "org.sqlite.JDBC";

    private Connection connection;
    private Statement statement;

    private Repository() {
        try {
            Class.forName(Repository.DRIVER);
        } catch (ClassNotFoundException e) {
            System.err.println("add SQLite driver to libs");
            throw new RuntimeException(e);
        }

        try {
            connection = DriverManager.getConnection(JDBC_URL);
            statement = connection.createStatement();
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
        try {
            statement.execute("DROP TABLE Request");
        } catch (SQLException e) {
        }
        try {
            statement.execute("CREATE TABLE IF NOT EXISTS Request (id INTEGER PRIMARY KEY AUTOINCREMENT, query text, counter bigint)");
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

    public void insert(String query, int count) throws SQLException {
        PreparedStatement preparedStatement = connection.prepareStatement("INSERT INTO Request(query,counter) VALUES ( ?, ?);");
        preparedStatement.setString(1, query);
        preparedStatement.setInt(2, count);
        int update = preparedStatement.executeUpdate();
        if (update == 0)
            System.out.println("Unsuccessful query");
    }

    public void showAll() throws SQLException {
        ResultSet result = statement.executeQuery("SELECT * FROM Request;");
        while (result.next()) {
            String query = result.getString("query");
            int count = result.getInt("counter");
            System.out.println(query + ", " + count);
        }
    }

    public void update(String query, int counter) throws SQLException {
        PreparedStatement preparedStatement = connection.prepareStatement("UPDATE Request SET counter = ? WHERE query = ?");
        preparedStatement.setInt(1, counter);
        preparedStatement.setString(2, query);
        int update = preparedStatement.executeUpdate();
        if (update == 0)
            System.out.println("Unsuccessful query");
    }

    synchronized public int getCounter(String query) throws SQLException {
        PreparedStatement preparedStatement = connection.prepareStatement("SELECT * FROM Request WHERE query = ?");
        preparedStatement.setString(1, query);
        ResultSet result = preparedStatement.executeQuery();
        if (result != null && result.next()) {
            return result.getInt("counter");
        } else
            return 0;
    }

    synchronized public void increment(String query) throws SQLException {
        int counter = getCounter(query);
        int newCounter = counter + 1;
        if (counter > 0)
            update(query, newCounter);
        else
            insert(query, newCounter);
    }
}