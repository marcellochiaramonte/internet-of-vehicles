package de.rub.enesys.ovms3lite.model;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.Entity;
import javax.persistence.ManyToOne;

@Entity
@Getter
@Setter
@NoArgsConstructor
public class ChargingStation extends BaseEntity {

    private Integer status;


    @ManyToOne
    private Location location;

}
