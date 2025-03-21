package de.rub.enesys.ovms3lite.model;


import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.GenericGenerator;
import org.hibernate.annotations.UpdateTimestamp;

import javax.persistence.*;
import java.time.LocalDateTime;
import java.time.ZonedDateTime;

@MappedSuperclass
@Getter
@Setter
@EqualsAndHashCode(of="uuid")
@Access(AccessType.FIELD)
@ToString
public abstract class BaseEntity {

    @Column(length = 70)
    @GeneratedValue(generator = "uuid2")
    @GenericGenerator(name="uuid2",strategy = "uuid2")
//    @GeneratedValue(strategy = GenerationType.AUTO)
    @Id
    private String uuid;




}