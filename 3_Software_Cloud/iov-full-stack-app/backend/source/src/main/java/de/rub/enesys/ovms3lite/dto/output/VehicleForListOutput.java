package de.rub.enesys.ovms3lite.dto.output;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class VehicleForListOutput {
    String id;
    String licensePlate;
    String carId;
    String model;
    String make;
    String iconColor;
}
