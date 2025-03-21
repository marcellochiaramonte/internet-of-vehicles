package de.rub.enesys.ovms3lite.repository;

import de.rub.enesys.ovms3lite.model.Metric;
import de.rub.enesys.ovms3lite.model.MetricId;
import de.rub.enesys.ovms3lite.model.Vehicle;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface MetricRepository extends CrudRepository<Metric,Long> {
    Optional<Metric> findOneById(Integer id);
}
