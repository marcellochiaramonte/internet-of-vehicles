package de.rub.enesys.ovms3lite.dto.input;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class VehicleEventInput {
    Long t;
    Integer id;
    String v;
}
