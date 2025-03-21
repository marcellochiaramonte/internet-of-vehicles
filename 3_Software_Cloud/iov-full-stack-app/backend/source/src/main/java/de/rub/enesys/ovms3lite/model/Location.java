package de.rub.enesys.ovms3lite.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Setter;

import javax.persistence.Entity;
import javax.persistence.ManyToOne;

@Entity
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Location extends BaseEntity{

    private Long timestamp;

    private Double latitude;
    private Double longitude;

    @JsonIgnore
    @ManyToOne
    private Vehicle vehicle;

}
