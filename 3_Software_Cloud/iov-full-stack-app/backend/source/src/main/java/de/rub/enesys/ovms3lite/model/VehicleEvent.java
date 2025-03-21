package de.rub.enesys.ovms3lite.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.*;
import org.hibernate.annotations.GenericGenerator;

import javax.persistence.*;
import java.io.Serializable;

@Entity
@Getter
@Setter
@NoArgsConstructor
public class VehicleEvent implements Serializable {

    @Id
    @Column(length = 70)
    @GeneratedValue(generator = "uuid2")
    @GenericGenerator(name="uuid2",strategy = "uuid2")
    private String uuid;

    private Long timestamp;

    private String value;

    @JsonIgnore
    @ManyToOne
    private Metric metric;

    @JsonIgnore
    @ManyToOne
    private Vehicle vehicle;


}
