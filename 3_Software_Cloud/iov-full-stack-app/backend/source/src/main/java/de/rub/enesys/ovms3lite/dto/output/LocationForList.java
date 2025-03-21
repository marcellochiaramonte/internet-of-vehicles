package de.rub.enesys.ovms3lite.dto.output;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class LocationForList {

    private Long timestamp;
    private Double latitude;
    private Double longitude;

}
