package de.rub.enesys.ovms3lite.model;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;

@Entity
@Getter
@Setter
@NoArgsConstructor
public class Metric{

    @Id
    @Column(unique = true)
    private Integer id;

    private String name;
    private String unitType;
    private String dataType;
}
