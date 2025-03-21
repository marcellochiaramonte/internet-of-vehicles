package de.rub.enesys.ovms3lite.repository;

import de.rub.enesys.ovms3lite.model.VehicleEvent;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface VehicleEventRepository extends CrudRepository<VehicleEvent,Long> {

}
