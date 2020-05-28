from pathlib import Path
import allel
import pandas as pd
import dask.array as da
import zarr
import gcsfs

# helper class to load phase 3 data
# doesn't get involved with storing data
# just exists to know where files are in relation to one another.
class release_data:
    
    release_dir = None
    gcs = None
    
    def __init__(self, release_path=Path("vo_agam_release/v3"), gcs_filesystem=gcsfs.GCSFileSystem()):
        # input checking
        if isinstance(release_path, str):
            release_path = Path(release_path)
        elif isinstance(release_path, Path):
            pass
        else:
            raise ValueError("`release_path` expects a string or pathlib.Path object")
        
        assert isinstance(gcs_filesystem, gcsfs.GCSFileSystem), "`gcs_filesystem` must be a gcsfs.GCSFileSystem object"
        
        self.release_dir = release_path
        self.gcs = gcs_filesystem
        
    def load_mask(self, seq_id, mask_id, filters_model="dt_20200416"):
    
        mask_path = self.release_dir / "site_filters" / filters_model / mask_id
        mask_store = self.gcs.get_mapper(mask_path.as_posix())
        mask_group = zarr.Group(mask_store)
        return da.from_zarr(mask_group[seq_id]["variants/filter_pass"])
    
    def load_variants_array(self, seq_id, field="POS", mask=None):
    
        """
        release_pa

        """

        path = self.release_dir / "snp_genotypes" / "all" / "sites"

        # need to open as mapping if this on cloud
        storez = self.gcs.get_mapper(path.as_posix())
        calldata = zarr.Group(storez)

        arr = da.from_zarr(calldata[f"{seq_id}/variants/{field}"])

        if mask is not None:
            
            assert isinstance(mask, da.core.Array), "mask must be a dask_array"
            arr = da.compress(mask, arr, axis=0).compute_chunk_sizes()

        return arr
    
    
    def load_calldata_by_sampleset(self, seq_id, sampleset, field="GT", mask=None):
    
        if isinstance(sampleset, str):

            path = self.release_dir / "snp_genotypes" / "all" / sampleset
            print(path)

            # need to open as mapping if this on cloud
            storez = self.gcs.get_mapper(path.as_posix())
            calldata = zarr.Group(storez)

            arr = da.from_zarr(calldata[f"{seq_id}/calldata/{field}"])
            
        elif isinstance(sampleset, list):
            arr = da.concatenate(
                [self.load_calldata_by_sampleset(seq_id, s, field=field, mask=None) for s in sampleset], axis=1)
        else:
            raise ValueError("sampleset must be a string, or a list of strings")

        if mask is not None:

            assert isinstance(mask, da.core.Array), "mask must be a dask_array"

            arr = da.compress(mask, arr, axis=0).compute_chunk_sizes()

        if field == "GT": 
            arr = allel.GenotypeDaskArray(arr)

        return arr
    
    def load_metadata_by_sampleset(
        self, sampleset, include_aim_species_calls=True, include_pca_species_calls=False, species_analysis="species_calls_20200422",
        convenience_species_assignment=True):
        
        if isinstance(sampleset, str):

            metadata_path = self.release_dir / "metadata" / "general" / sampleset / "samples.meta.csv"
            with self.gcs.open(metadata_path) as gcs_fh:
                df = pd.read_csv(gcs_fh, index_col=0)
                df["sampleset"] = sampleset

            if include_aim_species_calls:
                species_path_aim = self.release_dir / "metadata" / species_analysis / sampleset / "samples.species_aim.csv"
                with self.gcs.open(species_path_aim) as gcs_fh:
                    df_aim = pd.read_csv(gcs_fh, index_col=0)

            if include_pca_species_calls:
                species_path_pca = self.release_dir / "metadata" / species_analysis / sampleset / "samples.species_pca.csv"
                with self.gcs.open(species_path_pca) as gcs_fh:
                    df_pca = pd.read_csv(gcs_fh, index_col=0)

            if include_aim_species_calls and include_pca_species_calls:
                df_species = df_aim.join(df_pca, lsuffix='_aim', rsuffix='_pca')
                df = pd.concat([df, df_species], axis=1, sort=False)
                convenience_species_assignment = False
                print("Setting `convenience_species_assignment` to False. Using both PCA/AIM creates ambiguity.")
            elif include_aim_species_calls:
                df = pd.concat([df, df_aim], axis=1, sort=False)
            elif include_pca_species_calls:
                df = pd.concat([df, df_pca], axis=1, sort=False)
            else:
                convenience_species_assignment = False
                
            # only makes sense if exactly one of the include_species_call_x variables is true.
            if convenience_species_assignment:
                df["is_arabiensis"] = df.species_gambcolu_arabiensis == "arabiensis"
                df["is_gamb_colu"] = df.species_gambcolu_arabiensis == "gamb_colu"
                df["is_gambiae"] = df.species_gambiae_coluzzii == "gambiae"
                df["is_coluzzii"] = df.species_gambiae_coluzzii == "coluzzii"

            return df
        
        elif isinstance(sampleset, list):
            
            return pd.concat(
                [self.load_metadata_by_sampleset(s, include_aim_species_calls, include_pca_species_calls) for s in sampleset],
                axis=0, sort=False)
        