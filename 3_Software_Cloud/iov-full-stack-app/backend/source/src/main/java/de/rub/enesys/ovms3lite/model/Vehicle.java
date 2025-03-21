package de.rub.enesys.ovms3lite.model;

import lombok.*;

import javax.persistence.*;
import java.util.List;


@Entity
@ToString
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Vehicle {


    @Id
    @Column(length = 50, unique = true)
    private String id;

    @Column(length = 50, unique = true)
    private String licencePlate;

//    @Column(length = 50, unique = true)
    private String iconColor;

    private String model;
    private String make;

    @OneToMany(mappedBy = "vehicle",cascade = CascadeType.ALL,orphanRemoval = true)
    List<VehicleEvent> vehicleEventList;

    @OneToMany(mappedBy = "vehicle",cascade = CascadeType.ALL,orphanRemoval = true)
    List<Location> locationList;

}
