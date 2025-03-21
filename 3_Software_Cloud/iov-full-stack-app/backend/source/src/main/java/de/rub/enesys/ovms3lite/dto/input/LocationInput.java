package de.rub.enesys.ovms3lite.dto.input;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class LocationInput {
    Long t;
    Double lat;
    Double lon;
}
