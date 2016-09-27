from __future__ import print_function
from builtins import str
import sys
sys.path.insert(1,"../../../")
import h2o
from tests import pyunit_utils
from h2o.estimators.glrm import H2OGeneralizedLowRankEstimator

# I am trying to resolve a customer issue as captured in PUBDEV-3454.  Dmitry Tolstonogov (ADP)
# said that he ran a GLRM model on a data set (which he has shared with us but would not want
# us to put it out to public) with many categorical leves (~13000 columns in Y matrix).  Model
# converges in ~1 hour for 76 iterations but job runs for another 6.5 hours while nothing happens.
#  Bar indicates 10% done.
#
# The following test is written to duplicate this scenario and captured the stalling.  Once we
# found the cause and fix it, this test will be used to test our results with a different dataset
# with similar characteristic.


def glrm_PUBDEV_3454():
  features = ["emps_cnt", "client_revenue", "esdb_state", "esdb_zip", "revenue_adp", "status", "revenue_region",
              "business_unit", "naics3"]  # column names
  print("Importing user data...")
  datahex = \
    h2o.upload_file(pyunit_utils.locate("/Users/wendycwong/Documents/PUBDEV_3454_GLRM/glrm_data_DTolstonogov.csv"),
                    col_names=features)
  datahex.describe()

  glrm_h2o = H2OGeneralizedLowRankEstimator(k=9, loss="Quadratic", transform="STANDARDIZE", multi_loss="Categorical",
                                            model_name="clients_core_glrm", regularization_z="L2",
                                            regularization_y="L1", gamma_x=0.2, gamma_y=0.5, max_iterations=1000,
                                            init="SVD")
  glrm_h2o.train(x=features, training_frame=datahex)
  glrm_h2o.show()


if __name__ == "__main__":
  pyunit_utils.standalone_test(glrm_PUBDEV_3454)
else:
  glrm_iris()
