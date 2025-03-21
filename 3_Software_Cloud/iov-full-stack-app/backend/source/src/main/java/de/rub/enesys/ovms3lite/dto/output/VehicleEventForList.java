package de.rub.enesys.ovms3lite.dto.output;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class VehicleEventForList {
    private Long timestamp;
    private String value;
}
