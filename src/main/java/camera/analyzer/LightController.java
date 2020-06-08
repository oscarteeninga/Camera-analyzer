package camera.analyzer;

import com.mollin.yapi.YeelightDevice;
import com.mollin.yapi.exception.YeelightResultErrorException;
import com.mollin.yapi.exception.YeelightSocketException;

import java.util.GregorianCalendar;
import java.util.concurrent.atomic.AtomicBoolean;

public class LightController {
    private static final long TOGGLE_DELAY_MS = 1000L;
    private final YeelightDevice yeelightDevice;
    private AtomicBoolean last = new AtomicBoolean(true);
    private long lastToggleAt = 0;

    public LightController() throws YeelightSocketException {
        this.yeelightDevice = new YeelightDevice("192.168.1.39");
    }

    public void toggle() {
        if (canToggle()) {
            try {
                boolean newLast = !last.get();
                yeelightDevice.setPower(last.getAndSet(newLast));
            } catch (YeelightResultErrorException e) {
                e.printStackTrace();
            } catch (YeelightSocketException e) {
                e.printStackTrace();
            }
        }
    }

    private boolean canToggle() {
        long now = new GregorianCalendar().getTimeInMillis();
        if (Math.abs(lastToggleAt - now) > TOGGLE_DELAY_MS) {
            lastToggleAt = now;
            return true;
        }
        return false;
    }
}
