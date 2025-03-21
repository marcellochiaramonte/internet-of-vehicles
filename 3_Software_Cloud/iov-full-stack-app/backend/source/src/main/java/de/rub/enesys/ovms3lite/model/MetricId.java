package de.rub.enesys.ovms3lite.model;


public enum MetricId {
    CAR_ON(1),
    SOC(11),
    THREE(3);


    private final int value;

    MetricId(int value) {
        this.value = value;
    }

    public static MetricId getByValue(int i) {
        for (MetricId e : values()) {
            if (e.value == i) {
                return e;
            }
        }
        return null;
    }

//    CAR_ON,
//    POSITION
//    CAR_ON(1),
//    SPEED(2),
//    ODOMETER(3),
//    BATTERY_VOLTAGE(4),
//    BATTERY_CURRENT(5),
//    LOCATION(6);


//    int metric;
//    MetricId(int m) {
//        metric = m;
//    }
//    public int getMetric() {
//        return metric;
//    }

    }
