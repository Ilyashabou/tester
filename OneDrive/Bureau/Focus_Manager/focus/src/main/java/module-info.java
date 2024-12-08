module com.focus {
    requires javafx.controls;
    requires javafx.fxml;

    opens com.focus to javafx.fxml;
    exports com.focus;
}
